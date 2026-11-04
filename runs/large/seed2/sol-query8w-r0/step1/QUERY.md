# Phase 1 of 2: ask before you edit

The examples may fit more than one rule. Do NOT edit the model in this phase.
1. Write `CANDIDATES.md`: 2-4 distinct candidate rules for this step's behaviour
   change, each consistent with every labelled example you have.
2. Write `query.csv`: at most 8 input row(s), header = the feature names in the
   same order as `evidence.csv`, no label column. Choose the inputs whose correct
   labels best tell your candidates apart. Binary features must be 0 or 1; all
   other features must be in [0, 1].
You will then receive the correct labels in `answers.csv` and do the edit.

## Cover several kinds of rule
Your candidates must come from at least 3 of these kinds (one candidate per kind
at least), not variations of one kind:
- Output shift: add a constant or a region-dependent bonus to the current logit.
- Region override: force escalate or suppress inside a box of raw feature values.
- Input re-interpretation: the current model applied to modified inputs (one
  feature scaled, shifted or zeroed), possibly only when a condition holds.
- Interaction: one feature's effect on the decision depends on another feature.
Say which kind each candidate is. Pick queries that separate the kinds first, then values.
