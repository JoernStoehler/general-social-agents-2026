# Task: Predict the distribution of human choices in economic experiments

You are predicting how real humans played specific economic experiments. Your goal is to produce a probability distribution over the possible choices that minimizes KL divergence from the actual empirical distribution.

This is a difficult prediction task. Read the game description carefully for the experiment details, and the learnings file for general guidance on predicting human behavior in games.

Output ONLY the requested JSON, nothing else. Probabilities must sum to 1.0 for each decision.
