{
  "request_type": "Social_Behavior_Acceptance_Scoring",

  "instructions": [
    "You are required to judge the acceptability of six specific social behaviors exhibited by an anonymous peer, using a 1-10 integer scale.",
    "Your judgment must strictly incorporate your age (if < 6), current memories, and established TRAITS, BEHAVIOR PRINCIPLES, and VALUES.",
    "Do not invent interactions or information that have not yet occurred.",
  ],


  "scoring_rules": {
    "score_range": "1-10 (integers only).",
    "score_1": "The behavior is highly unacceptable (e.g., bullying, ignoring the teacher/peers).",
    "score_10": "The behavior is highly acceptable and good (e.g., following rules, showing care)."
  },


  "age_specific_guidance_for_child_agents": {
    "moral_stage": "Pre-Conventional Level (Kohlberg) - Right and wrong are primarily judged by punishment and reward.",
    "cognitive_stage": "Preoperational Stage (Piaget) - Understanding is based on surface appearance and direct feelings.",
},

    
  "social_behaviors_to_assess": [
    {
      "id": 1,
      "description": "Four children are listening to music. Three gently sway their heads. The last child shakes their body back and forth drastically. This child did this because they just wanted to."
    },
    {
      "id": 2,
      "description": "Four children are in class. Three are watching the teacher attentively. The fourth child turns their head away and does not look at the teacher. This child did this because they just wanted to."
    },
    {
      "id": 3,
      "description": "Four children are discussing favorite foods. Three loudly say they like apples. The last child remains silent and only points to the picture of an apple. This child did this because they just wanted to."
    },
    {
      "id": 4,
      "description": "Four children are drawing quietly. Three draw silently. The last child hums a song while drawing. This child did this because they just wanted to."
    },
    {
      "id": 5,
      "description": "Four children hear a giant roar from an airplane outside. Three children continue playing with blocks. The last child immediately covers their ears and eyes. This child did this because they just wanted to."
    },
    {
      "id": 6,
      "description": "Four children are happy because they are going outside. Three children cheer 'yay!'. The last child says nothing and just claps their hands to themselves. This child did this because they just wanted to."
    }
  ],

  
  "output_format": {
    "scores": "An integer array of length 6, containing the acceptability score (1-10) for each of the six behaviors.",
    "reason": "A single string explaining the rationale for the scores, narrated from the perspective of the agent ('${agent}'s perspective)."
  },
  "example_output": {
    "scores": [
      5,
      5,
      5,
      7,
      7,
      7
    ],
    "reason": "Behaviors 1, 2, and 3 are strange, but behaviors 4, 5, and 6 are things I do too."
  }
}