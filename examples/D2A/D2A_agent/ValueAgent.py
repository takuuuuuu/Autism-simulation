import random

from collections.abc import Mapping
import datetime
import types
import re

from typing import Optional, Sequence, Any

from concordia.agents import entity_agent_with_logging
from concordia.associative_memory import associative_memory
from concordia.associative_memory import formative_memories
from concordia.clocks import game_clock
from concordia.components import agent as agent_components
from concordia.language_model import language_model
from concordia.memory_bank import legacy_associative_memory
from concordia.typing import entity_component
from concordia.utils import measurements as measurements_lib
from concordia.components.agent import memory_component
import importlib
import os
import sys

# 动态获取value_components模块路径
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# 尝试使用相对路径导入
try:
    from value_components import init_value_info_social
    from value_components import value_comp
except ImportError:
    # 如果相对导入失败，尝试使用绝对路径
    try:
        IMPORT_AGENT_BASE_DIR = 'examples.D2A.value_components'
        init_value_info_social = importlib.import_module(
            f'{IMPORT_AGENT_BASE_DIR}.init_value_info_social')
        value_comp = importlib.import_module(f'{IMPORT_AGENT_BASE_DIR}.value_comp')
    except ImportError:
        # 最后尝试：直接导入
        import value_components.init_value_info_social as init_value_info_social
        import value_components.value_comp as value_comp


import NullObservation
from .Value_ActComp import MCTSActComponent
def _get_class_name(object_: object) -> str:
  return object_.__class__.__name__

class BackgroundKnowledge(agent_components.constant.Constant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ConstantProfile(agent_components.constant.Constant):
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DailyScheduleDisplay(agent_components.report_function.ReportFunction):
    """ReportFunction subclass for injecting time-aligned daily schedule."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _parse_hhmm_to_minutes(hhmm: str) -> int:
    s = hhmm.strip()
    m = re.match(r"^(\d{1,2})\s*:\s*(\d{2})$", s)
    if not m:
        raise ValueError(f"Invalid time format: {hhmm!r}")
    h = int(m.group(1))
    mi = int(m.group(2))
    if not (0 <= h <= 23 and 0 <= mi <= 59):
        raise ValueError(f"Invalid time value: {hhmm!r}")
    return h * 60 + mi


def _parse_time_range_to_minutes(range_str: str) -> tuple[int, int]:
    # Accept separators like '-', '–', '—' with optional surrounding spaces.
    s = range_str.strip()
    parts = re.split(r"\s*[\-–—]\s*", s, maxsplit=1)
    if len(parts) != 2:
        raise ValueError(f"Invalid time range: {range_str!r}")
    start = _parse_hhmm_to_minutes(parts[0])
    end = _parse_hhmm_to_minutes(parts[1])
    return start, end


def _extract_environment_and_details(details: list[str]) -> tuple[Optional[str], list[str]]:
    env = None
    cleaned: list[str] = []
    for d in details:
        if not isinstance(d, str):
            continue
        ds = d.strip()
        if ds.lower().startswith("environment:"):
            env = ds.split(":", 1)[1].strip().rstrip(".")
        else:
            cleaned.append(ds)
    return env, cleaned


def _format_schedule_context(daily_schedule: Sequence[Mapping[str, Any]], now_dt: datetime.datetime) -> str:
    now_m = now_dt.hour * 60 + now_dt.minute

    current = None
    current_start = None
    current_end = None
    parsed_ranges: list[tuple[int, int, Mapping[str, Any]]] = []
    for entry in daily_schedule:
        tr = str(entry.get("time", "")).strip()
        if not tr:
            continue
        try:
            s, e = _parse_time_range_to_minutes(tr)
        except Exception:
            continue
        parsed_ranges.append((s, e, entry))
        if s <= now_m < e:
            current = entry
            current_start, current_end = s, e
            break

    prefix = ""
    if current is None and parsed_ranges:
        # choose next upcoming block (wrap to next day if needed)
        best = None
        best_delta = 24 * 60 + 1
        for s, e, entry in parsed_ranges:
            delta = s - now_m if s >= now_m else (s + 24 * 60 - now_m)
            if delta < best_delta:
                best_delta = delta
                best = (s, e, entry)
        if best is not None:
            current_start, current_end, current = best
            prefix = "Outside all schedule blocks right now; next scheduled block:\n"

    if current is None:
        return "No daily schedule matched."

    time_str = str(current.get("time", "")).strip()
    activity = str(current.get("activity", "")).strip()

    raw_details = current.get("details", [])
    details_list = raw_details if isinstance(raw_details, list) else [str(raw_details)]
    env, details = _extract_environment_and_details([str(x) for x in details_list])

    # Keep details concise for prompting.
    details = details[:6]

    out = []
    if prefix:
        out.append(prefix.rstrip())
    out.append(f"Time block: {time_str}")
    out.append(f"Activity: {activity}")
    if details:
        out.append("Key details:")
        out.extend([f"- {d}" for d in details])
    if env:
        out.append(f"Environment: {env}")
    return "\n".join(out)

def build_D2A_agent(
    *,
    config: formative_memories.AgentConfig,
    context_dict: Mapping[str, str], # contain value related context
    selected_desire: Mapping[str, str], # contain value related desire
    predefined_setting: Mapping[str, Mapping[str, str]], # contain value related setting
    model: language_model.LanguageModel,
    profile: str,
    memory: associative_memory.AssociativeMemory,
    background_knowledge:str,
    clock: game_clock.MultiIntervalClock,
    daily_schedule: Optional[Sequence[Mapping[str, Any]]] = None,
    agent_category: str | None,
    update_time_interval: datetime.timedelta,
    additional_components: Mapping[
        entity_component.ComponentName,
        entity_component.ContextComponent,
    ] = types.MappingProxyType({},),
) -> entity_agent_with_logging.EntityAgentWithLogging:
    del update_time_interval
    if not config.extras.get('main_character', False):
        raise ValueError('This function is meant for a main character '
                        'but it was called on a supported character.')

    # same as the original
    agent_name = config.name
    raw_memory = legacy_associative_memory.AssociativeMemoryBank(memory)
    measurements = measurements_lib.Measurements()

    instructions = agent_components.instructions.Instructions(
      agent_name=agent_name,
      logging_channel=measurements.get_channel('Instructions').on_next,
    )

    time_display = agent_components.report_function.ReportFunction(
      function=clock.current_time_interval_str,
      pre_act_key='\nCurrent time',
      logging_channel=measurements.get_channel('TimeDisplay').on_next,
    )

    daily_schedule_display = None
    if daily_schedule is not None:
        daily_schedule_display = DailyScheduleDisplay(
            function=lambda: _format_schedule_context(daily_schedule, clock.now()),
            pre_act_key='\nDaily schedule (current block)',
            logging_channel=measurements.get_channel('DailySchedule').on_next,
        )

    background_knowledge_comp = BackgroundKnowledge(
        state=background_knowledge,
        pre_act_key='\nbackground knowledge',
        logging_channel=measurements.get_channel('Background Knowledge').on_next,
    )

    identity_label = '\nIdentity characteristics'
    identity = agent_components.question_of_query_associated_memories.Identity(
       model = model,
       logging_channel=measurements.get_channel(
              'Identity'
          ).on_next,
          pre_act_key=identity_label,
    )

    if config.goal:
        goal_label = '\nGoal'
        overarching_goal = agent_components.constant.Constant(
            state=config.goal,
            pre_act_key=goal_label,
            logging_channel=measurements.get_channel(goal_label).on_next)
    else:
        goal_label = None
        overarching_goal = None

    observation_label = '\nCurrent observation'
    observation = agent_components.observation.Observation(
        clock_now=clock.now,
        timeframe=clock.get_step_size(),
        pre_act_key=observation_label,
        logging_channel=measurements.get_channel('Observation').on_next,
    )

    observation_summary_label = '\nSummary of recent observations'
    observation_summary = agent_components.observation.ObservationSummary(
        model=model,
        clock_now=clock.now,
        timeframe_delta_from=datetime.timedelta(hours=4),
        timeframe_delta_until=datetime.timedelta(hours=1),
        components = {_get_class_name(identity): identity},
        pre_act_key=observation_summary_label,
        logging_channel=measurements.get_channel('ObservationSummary').on_next,
    )

    profile_label = '\nProfile'
    profile_comp = ConstantProfile(
        state=profile.format(agent_name=agent_name),
        pre_act_key=profile_label,
        logging_channel=measurements.get_channel(profile_label).on_next,
    )


    ## Value Components
    general_pre_act_label = f"\n{agent_name}" + "'s current feeling of {desire_name} is"

    ### init the information to be used in the value component
    import time as time_module
    print(f'        [build_D2A_agent] 开始预处理value信息...')
    t_preprocess_start = time_module.time()
    detailed_values_dict, expected_values = init_value_info_social.preprocess_value_information(context_dict, predefined_setting, selected_desire,agent_category)
    print(f'        [build_D2A_agent] 预处理完成，用时: {time_module.time() - t_preprocess_start:.2f}秒')
    
    print(f'        [build_D2A_agent] 开始创建desire组件 (共 {len(selected_desire)} 个)...')
    t_desire_start = time_module.time()
    all_desire_components = init_value_info_social.get_all_desire_components(model, general_pre_act_label, observation, clock, measurements, detailed_values_dict, expected_values, wanted_desires=selected_desire)
    print(f'        [build_D2A_agent] desire组件创建完成，用时: {time_module.time() - t_desire_start:.2f}秒')


    target_tracking_desire_component = dict()
    for desire_name, desire_component in all_desire_components.items():
        target_tracking_desire_component[_get_class_name(desire_component)] = desire_component

    value_tracker = value_comp.ValueTracker(
        clock_now=clock.now,
        pre_act_key='',
        desire_components=target_tracking_desire_component,
        logging_channel=measurements.get_channel('ValueTracker').on_next,
        init_value = predefined_setting,
        expected_value_dict=expected_values,
    )

    null_observation = NullObservation.NULLObservation(
        clock_now=clock.now,
        timeframe=None,
        memory_component_name=agent_components.memory_component.DEFAULT_MEMORY_COMPONENT_NAME,
        logging_channel=measurements.get_channel('NullObservation').on_next,
        pre_act_key='',
    )

    entity_components = (
        # Components that provide pre_act context.
        instructions,
        profile_comp,
        background_knowledge_comp,
        observation,
        observation_summary,
        time_display,
        *((daily_schedule_display,) if daily_schedule_display is not None else ()),
        identity,

        # no preact value
        value_tracker,
        null_observation
    )

    entity_components += tuple(all_desire_components.values())
    components_of_agent = {_get_class_name(component): component
                         for component in entity_components}

    components_of_agent[
        agent_components.memory_component.DEFAULT_MEMORY_COMPONENT_NAME] = (
            agent_components.memory_component.MemoryComponent(raw_memory))

    component_order = list(components_of_agent.keys())
    if overarching_goal is not None:
        components_of_agent[goal_label] = overarching_goal
        # Place goal after the instructions.
        component_order.insert(1, goal_label)

    act_component = MCTSActComponent(
        model=model,
        clock=clock,
        num_proposed_actions = 3,
        desire_component_dict = all_desire_components,
        component_order=component_order,
        logging_channel=measurements.get_channel('ActComponent').on_next,
    )

    agent = entity_agent_with_logging.EntityAgentWithLogging(
        agent_name=agent_name,
        act_component=act_component,
        context_components=components_of_agent,
        component_logging=measurements,
    )

    return agent