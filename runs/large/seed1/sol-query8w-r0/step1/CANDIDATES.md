# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Escalate when the candidate logit is greater than zero. Each rule below matches all 32 labelled examples. The examples do not establish which rule is correct.

1. **Input re-interpretation — ignore anger.** Set `tone_anger = 0` before evaluating the current model. Use `f(x with tone_anger = 0)` for every input.
2. **Output shift — apply an impact-dependent penalty.** Use `f(x) - 45` when `impact < 0.65`. Use `f(x) - 30` when `impact >= 0.65`. Keep all input values unchanged.
3. **Interaction — reduce the effect of anger.** Use `f(x) - 64 * tone_anger`. Thus, anger changes the escalation threshold in proportion to its value. Keep all input values unchanged.

The constants define provisional hypotheses. They are not confirmed correction parameters. No model weights were changed or fitted.

## Query design

Evidence row numbers below start at 1 and exclude the header. Each query copies an evidence row and changes only the stated features.

| Query row | Source row | Changes | Rule 1 label | Rule 2 label | Rule 3 label |
|---|---|---|---|---|---|
| 1 | 1 | `tone_anger = 0.25` | 0 | 0 | 1 |
| 2 | 1 | `tone_anger = 1` | 0 | 1 | 0 |
| 3 | 19 | `tone_anger = 0` | 1 | 0 | 1 |
| 4 | 19 | `tone_anger = 1` | 1 | 1 | 0 |
| 5 | 30 | `tone_anger = 0` | 1 | 0 | 1 |
| 6 | 30 | `tone_anger = 1` | 1 | 1 | 0 |
| 7 | 19 | `tone_anger = 0.5`, `impact = 0.64` | 1 | 0 | 1 |
| 8 | 19 | `tone_anger = 0.5`, `impact = 0.66` | 1 | 1 | 1 |

Rows 1–6 separate the three kinds of rule through different responses to anger. Rows 7–8 test the proposed impact threshold. Forward passes verified every prediction in this table.
