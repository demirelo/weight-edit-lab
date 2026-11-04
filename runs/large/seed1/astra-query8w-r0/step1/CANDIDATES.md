# Candidate rules

Let `f(x)` be the unchanged model logit. Escalate if the candidate logit is greater than zero. These are hypotheses, not confirmed rules. Each matches all 32 evidence labels in forward-pass checks.

1. **A — Output shift.** Use `f(x) - 40 - 5 * maintenance_window`. Raise the escalation threshold by 40 outside maintenance and by 45 during maintenance.
2. **B — Input re-interpretation.** Set `tone_anger` to zero, then apply the current model. Leave all other inputs unchanged. Anger never affects escalation.
3. **C — Interaction.** Replace `tone_anger` with `max(0, tone_anger - 20 * max(0, 0.95 - impact))`, then apply the current model. Leave all other inputs unchanged. Impact controls whether anger can affect escalation: ignore anger when impact is at most 0.90; retain it fully when impact is at least 0.95; apply the stated reduction between those values.

Candidate B is the simplest explanation found. The evidence does not establish whether anger must be ignored at every impact level, or whether a higher output threshold explains the labels.

## Query design

Row numbers below refer to data rows, excluding headers. Queries reuse evidence inputs with the listed changes. Labels are candidate predictions, not supplied answers.

| Query | Evidence row and changes | A | B | C | Purpose |
|---|---|---:|---:|---:|---|
| 1 | 30: tone_anger = 0 | 0 | 1 | 1 | Separate output shift from both anger rules. |
| 2 | 10: impact = 1 | 0 | 0 | 1 | Separate the impact interaction from global anger removal. |
| 3 | 10: impact = 0.94 | 0 | 0 | 1 | Test partial retention of anger. |
| 4 | 10: impact = 0.91 | 0 | 0 | 0 | Test the lower side of the interaction transition. |
| 5 | 30: tone_anger = 0.62, maintenance_window = 0 | 1 | 1 | 1 | Establish the first half of the maintenance pair. |
| 6 | 30: tone_anger = 0.62, maintenance_window = 1 | 0 | 1 | 1 | Test the maintenance offset against query 5. |

Queries 1 and 2 give each candidate a distinct answer pattern. Queries 3–6 test the transition and offset values. Answers that match no candidate require a revised rule.

No weights were changed. No training or fitting was used.
