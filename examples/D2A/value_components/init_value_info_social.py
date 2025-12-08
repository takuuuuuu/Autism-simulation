import random

from collections.abc import Mapping
import datetime
import types
import importlib
IMPORT_AGENT_BASE_DIR = 'examples.D2A.value_components'
init_value_info_social = importlib.import_module(
    f'{IMPORT_AGENT_BASE_DIR}.init_value_info_social')
value_comp = importlib.import_module(f'{IMPORT_AGENT_BASE_DIR}.value_comp')
from concordia.agents import entity_agent_with_logging
from concordia.associative_memory import associative_memory
from concordia.associative_memory import formative_memories
from concordia.clocks import game_clock
from concordia.components import agent as agent_components
from concordia.language_model import language_model
from concordia.memory_bank import legacy_associative_memory
from concordia.typing import entity_component
from concordia.utils import measurements as measurements_lib
# from concordia.components.agent.question_of_query_associated_memories import Identity, IdentityWithoutPreAct
# import value_comp
from concordia.components.agent import memory_component

profile_dict = {

}

decrease_map = {
    'extremely': 2,
    'quite': 1.5,
    'moderately': 1,
    'slightly': 0.5
}

values_names = [
    'sense of safety and attachment',
    'need for autonomy',
    'exploration and cognitive curiosity',
    'social interaction',
    'emotional expression',
]

values_names_descriptions = {
    'sense of safety and attachment':
        'The value of sense of safety and attachment ranges from 0 to 10. A score of 0 means the child feels insecure, afraid of separation, and unsure whether adults will provide comfort, while a score of 10 means the child feels deeply safe, supported, and confident that caregivers are reliably present.',

    'need for autonomy':
        'The value of need for autonomy ranges from 0 to 10. A score of 0 means the child feels unable to make choices or initiate activities, relying entirely on adults, while a score of 10 means the child feels empowered to make decisions, try tasks independently, and express their personal preferences.',

    'exploration and cognitive curiosity':
        'The value of exploration and cognitive curiosity ranges from 0 to 10. A score of 0 means the child shows little curiosity, hesitates to explore new objects, spaces, or ideas, while a score of 10 means the child is highly curious, eager to investigate the environment, ask questions, and learn through discovery.',

    'social interaction':
        'The value of social interaction ranges from 0 to 10. A score of 0 means the child feels disconnected from peers, avoids group play, or struggles to join social activities, while a score of 10 means the child actively engages with others, enjoys shared play, and feels comfortable participating in group routines.',

    'emotional expression':
        'The value of emotional expression ranges from 0 to 10. A score of 0 means the child has difficulty expressing feelings and may keep emotions inside or react unpredictably, while a score of 10 means the child can openly express emotions, communicate feelings to others, and seek help appropriately when upset.',

}

values_dict = values_names_descriptions


values_dict = values_names_descriptions
from pprint import pprint

def construct_all_profile_dict(wanted_desires: list[str], hidden_desires: list[str], predefined_desires: dict = None):
  if predefined_desires is not None:
    visual_desires_dict = predefined_desires['visual_desires_dict']
    hidden_desires_dict = predefined_desires['hidden_desires_dict']
    selected_profile_dict = predefined_desires['selected_desire_dict']
    traits_dict = predefined_desires['all_desire_traits_dict']

    traits = []
    for desire_name in visual_desires_dict.keys():
      _adj = selected_profile_dict[desire_name]['adj']
      _degree = traits_dict[_adj]
      append_str = f' is {_degree} {_adj}'
      traits.append("{agent_name}" + append_str)

    traits = '\n'.join(traits)
    return visual_desires_dict, hidden_desires_dict, selected_profile_dict, traits_dict, traits

  selected_profile_dict = dict() # key: desire, value: adj
  inverted_profile_dict = {desire: adj for adj, desire in profile_dict.items()}
  # pprint(f"inverted_profile_dict: {inverted_profile_dict}")
  for desire in wanted_desires:
    # pprint(f"desire: {desire}")
    desire_description = dict()
    desire_description['adj'] = inverted_profile_dict[desire]
    desire_description['description'] = values_dict[desire]
    selected_profile_dict[desire] = desire_description

  visual_desires = list(set(wanted_desires) - set(hidden_desires))
  visual_desires_dict = dict()
  for desire in visual_desires:
    visual_desires_dict[desire] = selected_profile_dict[desire]

  hidden_desires_dict = dict()
  for desire in hidden_desires:
    hidden_desires_dict[desire] = selected_profile_dict[desire]

  adj = [selected_profile_dict[desire_name]['adj'] for desire_name in selected_profile_dict.keys()]
  degree = ['extremely',
                'quite',
                'moderately',
                'slightly']

  traits_dict = dict()
  # contain both visual and hidden desires
  for i in range(len(adj)):
    _adj = adj[i]
    _degree = random.choice(degree)
    traits_dict[_adj] = _degree

#######################trait和value对应
  # only contain visual desires
  traits = []
  for desire_name in visual_desires:
    _adj = selected_profile_dict[desire_name]['adj']
    _degree = traits_dict[_adj]
    append_str = f' is {_degree} {_adj}'
    traits.append("{agent_name}" + append_str)

  traits = '\n'.join(traits)

  return (visual_desires_dict,
          hidden_desires_dict,
          selected_profile_dict,
          traits_dict,
          traits)




def _get_class_name(object_: object) -> str:
  return object_.__class__.__name__



def preprocess_value_information(context_dict, predefined_setting, selected_desires: list[str]):
    # profile_dict is in current file
    ### init the information to be used in the value component
    revert_profile_dict = {value: adj for adj, value in profile_dict.items()}
    expected_values = dict()

    # desires that should be reversed, i.e. the higher the value, the worse the situation
    should_reverse = [ ]

    # desires that should have a fixed expected value instead of using the default calculation
    fix_expected_value = {'sleepiness': 3,
                          'passion': 8}

    return_dict = dict()

    # print(f"predefined: {predefined_setting}") # desire name: initial value # selected desires
    # print(f"context: {context_dict}") # adj: degree of decrease # selected desires
    # print(f"decrease_map: {decrease_map}") # degree of decrease : step of decrease
    # pprint(f"revert_profile_dict: {revert_profile_dict}") # desire name: adj # all the desires
    # pprint(f"values_dict: {values_dict}") # desire name: description # all the desires
    # pprint(f"selected_desires: {selected_desires}") # selected desires

    for name, description in values_dict.items():
        detailed_desire_setting_dict = dict()
        if name not in selected_desires:
            continue
        adj_of_value = revert_profile_dict[name]
        detailed_desire_setting_dict['adj'] = adj_of_value
        # pprint(f"adj_of_value: {adj_of_value}")
        # pprint(f"context_dict: {context_dict}")
        degree_of_decrease = context_dict[adj_of_value]
        detailed_desire_setting_dict['degree of decrease'] = degree_of_decrease # qualitative value
        detailed_desire_setting_dict['step of decrease'] = decrease_map[degree_of_decrease] # numerical value
        detailed_desire_setting_dict['decrease time interval in hour'] = 1

        if name in ['spiritual satisfaction', 'social connectivity']:
            new_name = name
            detailed_desire_setting_dict['initial_value'] = predefined_setting[new_name]
        else:
            detailed_desire_setting_dict['initial_value'] = predefined_setting[name]
        detailed_desire_setting_dict['description'] = description
        if name in should_reverse:
            detailed_desire_setting_dict['reverse'] = True
            if name in fix_expected_value.keys():
                expected_values[name] = fix_expected_value[name]
            else:
                expected_values[name] = 3 - detailed_desire_setting_dict['step of decrease']
        else:
            detailed_desire_setting_dict['reverse'] = False
            if name in fix_expected_value.keys():
                expected_values[name] = fix_expected_value[name]
            else:
                expected_values[name] = 10 - (3 - detailed_desire_setting_dict['step of decrease'])

        return_dict[name] = detailed_desire_setting_dict

    return return_dict, expected_values


def get_all_desire_components_without_PreAct(model, general_pre_act_key:str, observation, clock, measurements, detailed_values_dict, expected_values, wanted_desires):
    return_dict = dict()

    for desire in wanted_desires:
      if desire == 'sense of safety and attachment':
        init = value_comp.SenseOfSafetyAndAttachmentWithoutPreAct
      elif desire == 'need for autonomy':
        init = value_comp.NeedForAutonomyWithoutPreAct
      elif desire == 'exploration and cognitive curiosity':
        init = value_comp.ExplorationAndCognitiveCuriosityWithoutPreAct
      elif desire == 'social interaction':
        init = value_comp.SocialInteractionWithoutPreAct
      elif desire == 'emotional expression':
        init = value_comp.EmotionalExpressionWithoutPreAct
      else:
        raise ValueError(f"Invalid desire: {desire}")

      Desire = init(
        model = model,
        pre_act_key=general_pre_act_key.format(desire_name = desire),
        observation_component_name=_get_class_name(observation),
        add_to_memory=False,
        memory_component_name = memory_component.DEFAULT_MEMORY_COMPONENT_NAME,
        init_value=detailed_values_dict[desire]['initial_value'],
        value_name=desire,
        description=detailed_values_dict[desire]['description'],
        decrease_step=detailed_values_dict[desire]['step of decrease'],
        decrease_interval=detailed_values_dict[desire]['decrease time interval in hour'],
        time_step=clock.get_step_size(),
        reverse=detailed_values_dict[desire]['reverse'],
        extra_instructions='',
        clock_now=clock.now,
        MAX_ITER=2,
        logging_channel=measurements.get_channel(desire).on_next,
    )
      return_dict[desire] = Desire

    return return_dict

def get_all_desire_components(model, general_pre_act_key:str, observation, clock, measurements, detailed_values_dict, expected_values, wanted_desires):
    # pprint(f"detailed_values_dict: {detailed_values_dict}")
    return_dict = dict()

    for desire in wanted_desires:
      if desire == 'sense of safety and attachment':
        init = value_comp.SenseOfSafetyAndAttachment
      elif desire == 'need for autonomy':
        init = value_comp.NeedForAutonomy
      elif desire == 'exploration and cognitive curiosity':
        init = value_comp.ExplorationAndCognitiveCuriosity
      elif desire == 'social interaction':
        init = value_comp.SocialInteraction
      elif desire == 'emotional expression':
         init = value_comp.EmotionalExpression
      else:
         raise ValueError(f"Invalid desire: {desire}")

      Desire = init(
        model = model,
        pre_act_key=general_pre_act_key.format(desire_name = desire),
        observation_component_name=_get_class_name(observation),
        add_to_memory=False,
        memory_component_name = memory_component.DEFAULT_MEMORY_COMPONENT_NAME,
        init_value=detailed_values_dict[desire]['initial_value'],
        value_name=desire,
        description=detailed_values_dict[desire]['description'],
        decrease_step=detailed_values_dict[desire]['step of decrease'],
        decrease_interval=detailed_values_dict[desire]['decrease time interval in hour'],
        time_step=clock.get_step_size(),
        reverse=detailed_values_dict[desire]['reverse'],
        extra_instructions='',
        clock_now=clock.now,
        MAX_ITER=1,
        logging_channel=measurements.get_channel(desire).on_next,
    )
      return_dict[desire] = Desire


    return return_dict
