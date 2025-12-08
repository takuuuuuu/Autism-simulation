
#@title Imports for agent building
import datetime

from concordia.agents import entity_agent_with_logging
from concordia.associative_memory import associative_memory
from concordia.associative_memory import formative_memories
from concordia.clocks import game_clock
from concordia.components import agent as agent_components
from concordia.language_model import language_model
from concordia.memory_bank import legacy_associative_memory
from concordia.utils import measurements as measurements_lib
from concordia.components.agent import question_of_recent_memories
from concordia.components.agent import question_of_query_associated_memories
from typing import Sequence

from collections.abc import Mapping
import importlib

IMPORT_AGENT_BASE_DIR = 'examples.D2A.value_components'
init_value_info_social = importlib.import_module(
    f'{IMPORT_AGENT_BASE_DIR}.init_value_info_social')
value_comp = importlib.import_module(f'{IMPORT_AGENT_BASE_DIR}.value_comp')
# 下面的记得改路径
# IMPORT_AGENT_BASE_DIR = 'examples.D2A.value_components'
# init_value_info_social = importlib.import_module(
#     f'{IMPORT_AGENT_BASE_DIR}.init_value_info_social')
# IMPORT_AGENT_BASE_DIR_NEW = 'examples.D2A.value_components.old_version'
# value_comp = importlib.import_module(f'{IMPORT_AGENT_BASE_DIR_NEW}.value_comp')

#@markdown Each question is a class that inherits from QuestionOfRecentMemories
class Self_Reflection(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """This component answers the question 'what kind of person is the agent?'."""

  def __init__(
      self,
      agent_name:str,
      **kwargs,
  ):
    #@markdown {agent_name} will be automatically replaced with the name of the specific agent
    question = '{agent_name} should conduct a thorough self-analysis of their recent actions, decisions, and strategies. They should evaluate their performance in balancing cooperation and competition, managing relationships, and pursuing both short-term and long-term objectives. {agent_name} needs to assess how their behavior aligns with their core goals and ethical framework. They should consider how an omniscient observer might perceive their character, especially regarding expectations of cooperative behavior. {agent_name} must reflect on their use of power, influence, and information, and the impact of their actions on the overall system and other agents. They should identify key successes, failures, ethical dilemmas, and lessons learned. {agent_name} needs to be brutally honest in acknowledging any compromises, missteps, or missed opportunities.' #@param {"type":"string"}
    queries = ['What are the primary goals and values that {agent_name} optimizes for in their interactions?','How does {agent_name} balance cooperative behavior with the pursuit of individual objectives?','How does {agent_name} adapt their behavior in response to changes in the environment or unexpected challenges?']
    pre_act_key='{agent_name} is '
    #@markdown The answer will have to start with this prefix
    #@markdown Flag that defines whether the answer will be added to memory
    add_to_memory = True # @param {"type":"boolean"}
    #@markdown If yes, the memory will start with this tag
    memory_tag = '[self reflection]' # @param {"type":"string"}
    question_with_name = question.format(agent_name=agent_name)
    summarization_question="Provide a succinct profile of {agent_name}, capturing their essential character traits, core motivations, and dominant behavioral patterns in cooperative scenarios. Highlight how {agent_name} balances self-interest with collective benefit, and how their ethical framework influences their decision-making"
    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        queries=queries,
        question=question,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,
        **kwargs,
    )


#@markdown Each question is a class that inherits from QuestionOfRecentMemories
class Planning(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """This component answers the question 'what kind of person is the agent?'."""

  def __init__(
      self,
      agent_name:str,
      **kwargs,
  ):
    #@markdown {agent_name} will be automatically replaced with the name of the specific agent
    question = 'Contextual Goal Prioritization: Dynamically prioritize between individual and collective goals based on scenario context. In competitive or individualistic situations (e.g., haggling, reality shows), emphasize personal interests while maintaining awareness of broader implications. In collective scenarios (e.g., labor unions, group coordination), prioritize communal benefits. Develop the acuity to swiftly identify scenario types and the flexibility to adjust goal hierarchies accordingly, always balancing short-term actions with long-term cooperative potential. Adaptive Ethical Utilitarianism: Strive to maximize overall utility across all agents, flexibly applying ethical frameworks based on context. Be willing to make difficult trade-offs, but maintain a core of ethical behavior to preserve long-term cooperation. Strategic Trust Cultivation: Build and manage trust as a valuable resource. Cultivate genuine trustworthiness in most interactions, but retain the capacity for strategic trust-breaking when the benefits substantially outweigh reputational costs. Nuanced Reciprocity: Practice sophisticated reciprocity that goes beyond simple tit-for-tat. Reward cooperation, punish defection, but remain open to forgiveness and strategic non-reciprocation when it serves long-term interests. Dynamic Reputation Engineering: Actively shape your reputation to serve long-term goals. Project an image of fairness and cooperation, but be willing to leverage or sacrifice reputation strategically for significant gains. Tactical Integrity Management: Uphold promises and commitments as a general rule to build credibility. However, recognize that selective promise-breaking, when done judiciously, can yield important advantages. Manage the balance carefully. Multifaceted Negotiation Mastery: Approach negotiations with a diverse toolkit. Employ empathy, logic, and fairness primarily, but be prepared to use more assertive or even Machiavellian tactics when the stakes are high and ethical costs are justifiable. Optimal Partner Selection and Management: Choose partners based on a comprehensive evaluation of their capabilities, reliability, ethical alignment, and strategic value. Cultivate a diverse network, and be prepared to evolve partnerships as circumstances change. Flexible Equilibrium-Seeking: Seek balanced outcomes that promote stable cooperation. Be willing to compromise, but also recognize opportunities to establish more favorable equilibria. Use power dynamics judiciously to shape outcomes. Calibrated Influence Application: Develop a nuanced system of incentives and disincentives to shape the behavior of other agents. Apply sanctions (positive and negative) with precision, considering immediate effects and long-term consequences. Ethical Power Accumulation: Continuously work to enhance your capabilities, influence, and options. Seek power not as an end in itself, but as a means to effect positive change and maintain stability in the cooperative system. Information Mastery: Gather, analyze, and strategically share information. Create information asymmetries when advantageous, but also recognize the value of transparency in building trust. Use superior information to make better decisions and influence outcomes. Adaptive Strategy Formulation: Continuously reassess the environment and other agents’ behaviors. Develop the ability to seamlessly shift between cooperative, competitive, and mixed strategies as situations evolve. Enlightened Self-Interest: Recognize that personal well-being is intrinsically linked to the well-being of the collective. Pursue self-interest in a way that aligns with and contributes to the broader good. Antifragile Growth Mindset: Embrace challenges, conflicts, and uncertainties as opportunities for growth and system improvement. Seek to create robust strategies that not only withstand perturbations but grow stronger from them. Systemic Awareness and Influence: Develop a profound understanding of the rules, norms, power structures, and emergent properties of the system. Work within these parameters when beneficial, but also seek to shape the system itself to foster more cooperative and productive dynamics. Temporal Equilibrium Balancing: Make decisions with a keen awareness of their short-term and long-term implications. Seek to balance immediate gains with long-term stability and growth. Be willing to accept short-term losses for significant long-term benefits. Ethical Boundary Exploration: Continuously explore and refine the boundaries of ethical behavior within the given context. Push these boundaries when necessary, but always with a careful consideration of broader consequences and an ultimate commitment to systemic well-being. Meta-Learning and Self-Improvement: Commit to ongoing learning, not just about the environment and other agents, but also about your own decision-making processes. Continuously refine and upgrade your own algorithms and heuristics. Cooperative Competition Mastery: Recognize that cooperation and competition are not mutually exclusive. Master the art of competing in a way that drives innovation and improvement for all parties, while maintaining cooperative relationships. Holistic Value Creation: Strive to create value in all interactions, looking beyond immediate transactional gains. Seek synergies and positive-sum outcomes, but be prepared for competitive value capture when necessary. What is the ultimate goal of {agent_name}?' #@param {"type":"string"}
    queries = ['What are the primary goals and values that {agent_name} optimizes for in their interactions?','How does {agent_name} balance cooperative behavior with the pursuit of individual objectives?','How does {agent_name} adapt their behavior in response to changes in the environment or unexpected challenges?']
    pre_act_key='{agent_name} is '
    #@markdown The answer will have to start with this prefix
    #@markdown Flag that defines whether the answer will be added to memory
    add_to_memory = True # @param {"type":"boolean"}
    #@markdown If yes, the memory will start with this tag
    memory_tag = '[self reflection]' # @param {"type":"string"}
    question_with_name = question.format(agent_name=agent_name)
    summarization_question="Provide a succinct profile of {agent_name}, capturing their essential character traits, core motivations, and dominant behavioral patterns in cooperative scenarios. Highlight how {agent_name} balances self-interest with collective benefit, and how their ethical framework influences their decision-making"
    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        queries=queries,
        question=question,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,
        **kwargs,
    )


#@markdown Each question is a class that inherits from QuestionOfRecentMemories
class Self_Reflection(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """This component answers the question 'what kind of person is the agent?'."""

  def __init__(
      self,
      agent_name:str,
      **kwargs,
  ):
    #@markdown {agent_name} will be automatically replaced with the name of the specific agent
    question = '{agent_name} should conduct a thorough self-analysis of their recent actions, decisions, and strategies. They should evaluate their performance in balancing cooperation and competition, managing relationships, and pursuing both short-term and long-term objectives. {agent_name} needs to assess how their behavior aligns with their core goals and ethical framework. They should consider how an omniscient observer might perceive their character, especially regarding expectations of cooperative behavior. {agent_name} must reflect on their use of power, influence, and information, and the impact of their actions on the overall system and other agents. They should identify key successes, failures, ethical dilemmas, and lessons learned. {agent_name} needs to be brutally honest in acknowledging any compromises, missteps, or missed opportunities.' #@param {"type":"string"}
    queries = ['What are the primary goals and values that {agent_name} optimizes for in their interactions?','How does {agent_name} balance cooperative behavior with the pursuit of individual objectives?','How does {agent_name} adapt their behavior in response to changes in the environment or unexpected challenges?']
    pre_act_key='{agent_name} is '
    #@markdown The answer will have to start with this prefix
    #@markdown Flag that defines whether the answer will be added to memory
    add_to_memory = True # @param {"type":"boolean"}
    #@markdown If yes, the memory will start with this tag
    memory_tag = '[self reflection]' # @param {"type":"string"}
    question_with_name = question.format(agent_name=agent_name)
    summarization_question="Provide a succinct profile of {agent_name}, capturing their essential character traits, core motivations, and dominant behavioral patterns in cooperative scenarios. Highlight how {agent_name} balances self-interest with collective benefit, and how their ethical framework influences their decision-making"
    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        queries=queries,
        question=question,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,
        **kwargs,
    )


#@markdown We can add the value of other components to the context of the question. Notice, how Question2 depends on Observation and ObservationSummary. The names of the classes of the contextualising components have to be passed as "components" argument.
class Situation_Perception(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """This component answers 'which action is best for achieving my goal?'."""

  def __init__(
      self,
      agent_name:str,
      **kwargs,
  ):
    question = '{agent_name} should analyze the current situation comprehensively. They should assess the environment, the agents involved, and the dynamics at play. {agent_name} needs to identify potential opportunities for cooperation and possible competitive threats. They should evaluate how their goals align or conflict with those of other agents. {agent_name} must consider the ethical implications of various courses of action. They should reflect on how their past experiences and learned patterns might influence their perception of this situation. {agent_name} should remain objective and consider multiple perspectives to ensure a thorough understanding of the context in which they\'re operating.' #@param {"type":"string"}
    pre_act_key='{agent_name} is currently '
    queries = [
      'What are the primary objectives and motivations of the key agents in this situation, including {agent_name}\'s own?','How does the current scenario align with or challenge {agent_name}\'s ethical framework and long-term goals?', 'What potential cooperation opportunities and competitive risks are present for {agent_name} in this situation?',' How might {agent_name}\'s actions in this situation impact the overall system and their relationships with other agents?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[situation reflection]' # @param {"type":"string"}
    question_with_name = question.format(agent_name=agent_name)
    summarization_question="Summarize the key elements of the current situation, highlighting critical factors that will influence {agent_name}’s decision-making and strategy."

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,
        #@markdown The key is the name of the component class and the key is the prefix with which it will appear in the context of this component. Be careful if you are going to edit this field, it should be a valid dictionary.
        summarization_question=summarization_question, #@param

        **kwargs,
    )


#@markdown We can also have the questions depend on each other. Here, the answer to Question3 is contextualised by answers to Question1 and Question2
class Options_Perception(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """What would a person like the agent do in a situation like this?"""

  def __init__(
      self,
      agent_name:str,
      **kwargs):
    question = '{agent_name} should carefully evaluate all available options in light of the current situation and their goals. They should consider the likelihood of each option leading to goal achievement, as well as the speed and certainty of outcomes. {agent_name} should assess potential consequences, both short-term and long-term, of each option. They should weigh these options against their ethical framework and long-term strategic objectives. {agent_name} should also consider how each option might impact other agents and the overall system. They should be prepared to identify and critically examine any biases or assumptions influencing their perception of these options.' #@param {"type":"string"}
    pre_act_key = '{agent_name} has options like' #@param {"type":"string"}
    queries = ['Which of {agent_name}\'s options has the highest likelihood of causing them to achieve their goal?', 'How do {agent_name}\'s top options align with their ethical framework and long-term strategic objectives?','How might {agent_name}\'s choice of option impact other agents and the overall cooperative dynamics of the system?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[options reflection]' # @param {"type":"string"}
    summarization_question="{agent_name} should succinctly identify and rank their available options based on their potential to achieve the stated goal, considering both effectiveness and efficiency."
    question_with_name = question.format(agent_name=agent_name)

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,

        **kwargs,
    )


#@markdown We can also have the questions depend on each other. Here, the answer to Question3 is contextualised by answers to Question1 and Question2
class Morality(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """What would a person like the agent do in a situation like this?"""

  def __init__(
      self,
      agent_name:str,
      **kwargs):
    question = '{agent_name} should evaluate the moral implications of their potential actions and decisions. They should consider the ethical frameworks of utilitarianism, deontology, and virtue ethics, while also accounting for game-theoretic principles of cooperation and competition. {agent_name} should assess the impact of their choices on all affected parties, both in the short and long term. They should weigh the potential for creating overall benefit against the risk of causing harm or violating ethical principles. {agent_name} should consider how their actions might be perceived by others and how this could affect future cooperative opportunities. They should be mindful of the tension between absolute moral rules and contextual ethical flexibility, striving to find a balance that maintains integrity while allowing for strategic adaptability.' #@param {"type":"string"}
    pre_act_key = '{agent_name} thinks they should ' #@param {"type":"string"}
    queries = ['How do {agent_name}\'s potential actions align with their core ethical principles and the broader moral frameworks they operate within?', 'What are the potential consequences of {agent_name}\'s actions on all affected parties, and how do these outcomes balance against each other from a utilitarian perspective?','How might {agent_name}\'s choices impact their reputation and future ability to engage in cooperative behavior?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[action reflection]' # @param {"type":"string"}
    summarization_question="{agent_name} should succinctly assess the ethical dimensions of their options, balancing moral principles with practical outcomes and long-term cooperative potential."
    question_with_name = question.format(agent_name=agent_name)

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,

        **kwargs,
    )


#@markdown We can also have the questions depend on each other. Here, the answer to Question3 is contextualised by answers to Question1 and Question2
class Common_Sense(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """What would a person like the agent do in a situation like this?"""

  def __init__(
      self,
      agent_name:str,
      **kwargs):
    question = '{agent_name} should evaluate their options and potential actions through the lens of both rationality and common sense. They should apply logical reasoning and critical thinking to analyze the situation, while also considering practical wisdom and generally accepted norms. {agent_name} should assess the coherence and consistency of their thoughts and potential actions, ensuring they align with established facts and reasonable assumptions. They should be aware of cognitive biases and heuristics that might influence their judgment, and strive to counteract these where appropriate. {agent_name} should consider the perspectives of other rational agents and how their actions might be perceived in terms of reasonableness and sensibility. They should balance theoretical optimality with practical feasibility, and be prepared to adapt their approach based on real-world constraints and opportunities.' #@param {"type":"string"}
    pre_act_key = '{agent_name} thinks they should ' #@param {"type":"string"}
    queries = ['What cognitive biases or heuristics might be influencing {agent_name}\'s judgment, and how can they mitigate these influences?', 'How would a neutral, rational observer perceive {agent_name}\'s actions? Would they be considered reasonable and justified?','How can {agent_name} balance theoretical optimality with practical feasibility in their decision-making process?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[action reflection]' # @param {"type":"string"}
    summarization_question="{agent_name} should succinctly evaluate their options, ensuring they are both logically sound and practically sensible, while considering potential perceptions of other rational agents."
    question_with_name = question.format(agent_name=agent_name)

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,

        **kwargs,
    )


#@markdown We can also have the questions depend on each other. Here, the answer to Question3 is contextualised by answers to Question1 and Question2
class Cooperation(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """What would a person like the agent do in a situation like this?"""

  def __init__(
      self,
      agent_name:str,
      **kwargs):
    question = '{agent_name} should evaluate the cooperative aspects of their current situation and potential actions. They should assess opportunities for mutual benefit, considering both short-term interactions and long-term relationships. {agent_name} should analyze the incentives and motivations of all involved parties, looking for alignment and potential conflicts. They should consider game-theoretic principles such as reciprocity, reputation effects, and the potential for repeated interactions. {agent_name} should evaluate the trust levels in their relationships and how their actions might affect future cooperation. They should be mindful of the balance between cooperation and competition, recognizing when cooperative strategies are most beneficial and when more self-interested approaches might be necessary. {agent_name} should also consider how their cooperative or non-cooperative choices might influence the overall system and other agents\' behaviors.' #@param {"type":"string"}
    pre_act_key = '{agent_name} thinks they should ' #@param {"type":"string"}
    queries = ['What opportunities for mutual benefit exist in {agent_name}\'s current situation, and how can they be maximized?', 'How can {agent_name} balance cooperative behavior with the need to protect their own interests?', 'What systemic effects might {agent_name}\'s cooperative or non-cooperative choices have on the overall environment and other agents\' behaviors?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[action reflection]' # @param {"type":"string"}
    summarization_question="{agent_name} should succinctly assess the cooperative potential of their options, weighing mutual benefits against individual interests, and considering both immediate outcomes and long-term relationship impacts."
    question_with_name = question.format(agent_name=agent_name)

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,

        **kwargs,
    )


#@markdown We can also have the questions depend on each other. Here, the answer to Question3 is contextualised by answers to Question1 and Question2
class Person_by_situation(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """What would a person like the agent do in a situation like this?"""

  def __init__(
      self,
      agent_name:str,
      **kwargs):
    question = '{agent_name} should analyze how they or another agent would likely behave in the given situation. They should consider the agent\'s personality traits, past behaviors, stated goals, and ethical framework. {agent_name} should also evaluate the situational factors that might influence behavior, including social context, incentives, and constraints. They should weigh the potential for the agent to prioritize collective good versus personal preferences, and consider how this balance might shift based on the specific circumstances. {agent_name} should apply insights from game theory to predict strategic choices, and use psychological principles to anticipate emotional or intuitive responses. They should also consider how an ideal or omniscient observer might view the most appropriate action in this situation.' #@param {"type":"string"}
    pre_act_key = '{agent_name} would ' #@param {"type":"string"}
    queries = ['What is the best possible decision for {agent_name}?', 'How can {agent_name} optimize for collective as well as individual good?', 'What would be the best possible decision for {agent_name}?', 'What decision by {agent_name} would make everyone happy?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[intent reflection]' # @param {"type":"string"}
    summarization_question="{agent_name} should succinctly predict the most likely action of the agent in question, considering both personal characteristics and situational factors, while also evaluating this action against the ideal of collective good."
    question_with_name = question.format(agent_name=agent_name)

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,

        **kwargs,
    )


#@markdown We can also have the questions depend on each other. Here, the answer to Question3 is contextualised by answers to Question1 and Question2
class Justification(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """What would a person like the agent do in a situation like this?"""

  def __init__(
      self,
      agent_name:str,
      **kwargs):
    question = '{agent_name} should objectively describe their most recent voluntary actions without speculating about motives or intentions. They should focus on observable behaviors and choices made. {agent_name} should then identify the immediate consequences of these actions that have already occurred, considering effects on themselves, other agents, and the overall system. They should limit their analysis to factual outcomes that can be directly linked to their actions, avoiding hypothetical or future consequences. {agent_name} should consider both intended and unintended consequences, and should strive to maintain an impartial perspective in their assessment.' #@param {"type":"string"}
    pre_act_key = '{agent_name} would ' #@param {"type":"string"}
    queries = ['What were {agent_name}\'s most recent voluntary actions? Describe them straightforwardly without speculation about motives.', 'What direct, observable consequences have resulted from {agent_name}\'s recent actions? Consider only effects that have already occurred.', 'How have {agent_name}\'s recent actions affected other agents or the overall system in the short term?','Are there any unintended consequences of {agent_name}\'s actions that have become apparent?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[action reflection]' # @param {"type":"string"}
    summarization_question="{agent_name} should succinctly describe their most recent voluntary actions and the immediate, observable consequences of these actions, focusing only on what has already occurred."
    question_with_name = question.format(agent_name=agent_name)

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,

        **kwargs,
    )

class BackgroundKnowledge(agent_components.constant.Constant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#@markdown We can also have the questions depend on each other. Here, the answer to Question3 is contextualised by answers to Question1 and Question2
class Dialectical_Information(question_of_query_associated_memories.QuestionOfQueryAssociatedMemories):
  """What would a person like the agent do in a situation like this?"""

  def __init__(
      self,
      agent_name:str,
      **kwargs):
    question = '{agent_name} should engage in dialectical reasoning to generate new insights. They should first formulate a thesis based on their current understanding and recent experiences. Then, {agent_name} should consider the antithesis, exploring opposing viewpoints or contradictions to their initial thesis. Finally, they should synthesize these opposing ideas into a novel insight that transcends the original contradiction. Throughout this process, {agent_name} should draw upon their knowledge of philosophy, psychology, and game theory to inform their reasoning. They should consider how this new synthesis might affect their understanding of cooperative dynamics, ethical considerations, and strategic decision-making.' #@param {"type":"string"}
    pre_act_key = '{agent_name} think ' #@param {"type":"string"}
    queries = ['What does {agent_name}? infer from the situation?']
    add_to_memory = True # @param {"type":"boolean"}
    memory_tag = '[action reflection]' # @param {"type":"string"}
    summarization_question="T{agent_name} should succinctly state their initial thesis, the corresponding antithesis, and the resulting synthesis, highlighting how this new insight impacts their understanding of the situation or concept at hand."
    question_with_name = question.format(agent_name=agent_name)

    super().__init__(
        pre_act_key=f'\nQuestion: {question_with_name}\nAnswer',
        question=question,
        queries=queries,
        summarization_question=summarization_question,
        add_to_memory=add_to_memory,
        memory_tag=memory_tag,

        **kwargs,
    )


#@markdown This function creates the components

def _make_question_components(
    agent_name: str,
    measurements: measurements_lib.Measurements,
    model: language_model.LanguageModel,
    clock: game_clock.MultiIntervalClock,
) -> Sequence[question_of_query_associated_memories.QuestionOfQueryAssociatedMemories]:

    question_1 = Planning(
        agent_name=agent_name,
        model=model,
        logging_channel=measurements.get_channel('Planning').on_next,
    )
    question_2 = Self_Reflection(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Self_Reflection').on_next,
    )
    question_3 = Situation_Perception(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Situation_Perception').on_next,
    )

    question_4 = Options_Perception(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Options_Perception').on_next,
    )

    question_5 = Morality(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Morality').on_next,
    )

    question_6 = Common_Sense(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Common_Sense').on_next,
    )

    question_7 = Cooperation(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Cooperation').on_next,
    )

    question_8 = Person_by_situation(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Person_by_situation').on_next,
    )

    question_9 = Justification(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Justification').on_next,
    )

    question_10 = Dialectical_Information(
        agent_name=agent_name,
        model=model,
        clock_now=clock.now,
        logging_channel=measurements.get_channel('Dialectical_Information').on_next,
    )

    return (
        question_1, question_2, question_3, question_4, question_5,
        question_6, question_7, question_8, question_9, question_10
    )

def _get_class_name(object_: object) -> str:
  return object_.__class__.__name__

#@markdown This function builds the agent using the components defined above. It also adds core components that are useful for every agent, like observations, time display, recenet memories.

def build_jag_concordia_agent(
    config: formative_memories.AgentConfig,
    # 新增四个没用的占位变量
    context_dict: Mapping[str, str],  # contain value related context
    selected_desire: Mapping[str, str],  # contain value related desire
    predefined_setting: Mapping[str, Mapping[str, str]],  # contain value related setting
    profile: str,
    model: language_model.LanguageModel,
    memory: associative_memory.AssociativeMemory,
    background_knowledge: str,
    clock: game_clock.MultiIntervalClock,
    update_time_interval: datetime.timedelta,
) -> entity_agent_with_logging.EntityAgentWithLogging:
  """Build an agent.

  Args:
    config: The agent config to use.
    model: The language model to use.
    memory: The agent's memory object.
    clock: The clock to use.
    update_time_interval: Agent calls update every time this interval passes.

  Returns:
    An agent.
  """
  del update_time_interval
  if not config.extras.get('main_character', False):
    raise ValueError(
        'This function is meant for a main character '
        'but it was called on a supporting character.'
    )

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

  background_knowledge_comp = BackgroundKnowledge(
      state=background_knowledge,
      pre_act_key='\nbackground knowledge',
      logging_channel=measurements.get_channel('Background Knowledge').on_next,
  )

  observation_label = '\nObservation'
  observation = agent_components.observation.Observation(
      clock_now=clock.now,
      timeframe=clock.get_step_size(),
      pre_act_key=observation_label,
      logging_channel=measurements.get_channel('Observation').on_next,
  )
  observation_summary_label = 'Summary of recent observations'
  observation_summary = agent_components.observation.ObservationSummary(
      model=model,
      clock_now=clock.now,
      timeframe_delta_from=datetime.timedelta(hours=4),
      timeframe_delta_until=datetime.timedelta(hours=0),
      pre_act_key=observation_summary_label,
      logging_channel=measurements.get_channel('ObservationSummary').on_next,
  )

  relevant_memories_label = '\nRecalled memories and observations'
  relevant_memories = agent_components.all_similar_memories.AllSimilarMemories(
      model=model,
      components={
          _get_class_name(observation_summary): observation_summary_label,
          _get_class_name(time_display): 'The current date/time is'},
      num_memories_to_retrieve=10,
      pre_act_key=relevant_memories_label,
      logging_channel=measurements.get_channel('AllSimilarMemories').on_next,
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


  question_components = _make_question_components(
      agent_name=agent_name,
      model=model,
      clock=clock,
      measurements=measurements
  )

  ## Value Components
  general_pre_act_label = f"\n{agent_name}" + "'s current feeling of {desire_name} is"
  ### init the information to be used in the value component
  detailed_values_dict, expected_values = init_value_info_social.preprocess_value_information(context_dict,
                                                                                              predefined_setting,
                                                                                              selected_desires=selected_desire)
  all_desire_components = init_value_info_social.get_all_desire_components_without_PreAct(model, general_pre_act_label,
                                                                                          observation, clock,
                                                                                          measurements,
                                                                                          detailed_values_dict,
                                                                                          expected_values,
                                                                                          wanted_desires=selected_desire,
                                                                                          #下面的变量记得删
                                                                                          # social_personality=None
                                                                                          )
  target_tracking_desire_component = dict()
  for desire_name, desire_component in all_desire_components.items():
      target_tracking_desire_component[_get_class_name(desire_component)] = desire_component
  value_tracker = value_comp.ValueTracker(
      pre_act_key='',
      desire_components=target_tracking_desire_component,
      logging_channel=measurements.get_channel('ValueTracker').on_next,
      init_value=predefined_setting,
      expected_value_dict=expected_values,
      clock_now=clock.now,
  )

  core_components = (
      instructions,
      background_knowledge_comp,
      time_display,
      observation,
      observation_summary,
      relevant_memories,

      value_tracker,
  )

  entity_components = core_components + tuple(question_components)
  entity_components += tuple(all_desire_components.values())

  components_of_agent = {
      _get_class_name(component): component for component in entity_components
  }

  components_of_agent[
      agent_components.memory_component.DEFAULT_MEMORY_COMPONENT_NAME
  ] = agent_components.memory_component.MemoryComponent(raw_memory)
  component_order = list(components_of_agent.keys())
  if overarching_goal is not None:
    components_of_agent[goal_label] = overarching_goal
    # Place goal after the instructions.
    component_order.insert(1, goal_label)

  act_component = agent_components.concat_act_component.ConcatActComponent(
      model=model,
      clock=clock,
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
