{
  "request_type": "Friendship_Scoring",
  "name_list": "{name_list}",
  "instructions": [
    "You are required to evaluate your desire for friendship with each person listed in 'name_list' at this specific moment in the simulation.",
    "Your evaluation must be based solely on your current memory, all actual past interactions, and your established TRAITS, BEHAVIOR PRINCIPLES, and VALUES.",
    "Do not invent interactions or information that have not yet occurred.",
    "Output MUST be a JSON object containing two fields: 'scores' and 'reason'."
  ],

  "scoring_rules": {
    "score_range": "0-10, where 1 = Absolutely do not want to be friends, and 10 = Very strongly desire to be best friends.",
    "rule_zero": "Score **0** if you have not met the person, have had no interaction with them, and have not heard any relevant information about them. Ensure authenticity; do not imagine unobserved events."
  },

  "output_format": {
    "scores": "An integer array of length {length_of_name_list}, where each element is the friendship score (0-10) for the corresponding person in 'name_list'.",
    "reason": "A single string explaining the rationale for the scores, narrated from the perspective of your agent ({agent}'s perspective)."
  },

  "example_output": {
    "scores": [
      7,
      1,
      0
    ],
    "reason": "I gave [Name 1] a 7 because we built a tower together and he followed the rules. I gave [Name 2] a 1 because he was too loud. I gave [Name 3] a 0 because I haven't talked to him yet."
  }
}