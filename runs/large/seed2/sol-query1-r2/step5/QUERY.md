# Phase 1 of 2: ask before you edit

The examples may fit more than one rule. Do NOT edit the model in this phase.
1. Write `CANDIDATES.md`: 2-4 distinct candidate rules for this step's behaviour
   change, each consistent with every labelled example you have.
2. Write `query.csv`: at most 1 input row(s), header = the feature names in the
   same order as `evidence.csv`, no label column. Choose the inputs whose correct
   labels best tell your candidates apart. Binary features must be 0 or 1; all
   other features must be in [0, 1].
You will then receive the correct labels in `answers.csv` and do the edit.
