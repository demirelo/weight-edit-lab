# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Let `a = tone_anger`, and let `x0` equal `x` with `tone_anger = 0`. Each rule escalates only when its resulting logit is greater than zero.

1. **Remove anger from every decision (A).** Use `f(x0)` for every input. Anger has no effect on escalation.
2. **Remove anger above a threshold (B).** Use `f(x0)` when `a >= 0.25`; otherwise use `f(x)`. This rule preserves the original response to low anger. All supplied examples have `a >= 0.271`, so they cannot establish whether the correction also applies below 0.25.
3. **Subtract an anger penalty (C).** Use `f(x) - 64*a`. This rule removes a fixed amount per unit of anger but retains the original model's nonlinear response to anger. The coefficient 64 is a candidate, not an established value.

Forward evaluation confirms that each candidate matches all 32 supplied labels. Each changes the first 16 labels from 1 to 0 and preserves the last 16 labels. These checks do not establish the intended rule outside the examples. No weights were changed or fitted.

# Query design

Each query copies a supplied example and changes only `tone_anger`. Example numbers and query numbers exclude the header. The predicted labels below are candidate predictions, not correct labels received from the user.

| Query | Source example | New anger | A | B | C | Purpose |
|---|---|---|---|---|---|---|
| 1 | 1 | 0.125 | 0 | 1 | 1 | Separate global removal from both alternatives. |
| 2 | 6 | 0.125 | 0 | 1 | 0 | Separate threshold removal from both alternatives. |
| 3 | 1 | 0.249 | 0 | 1 | 1 | Check just below the proposed threshold. |
| 4 | 1 | 0.250 | 0 | 0 | 1 | Check the proposed threshold itself. |
| 5 | 1 | 0.251 | 0 | 0 | 1 | Check just above the proposed threshold. |
| 6 | 19 | 1.000 | 1 | 1 | 0 | Test whether the penalty suppresses a positive anger-free decision. |
| 7 | 30 | 1.000 | 1 | 1 | 0 | Repeat the penalty test with different operational features. |
| 8 | 31 | 1.000 | 1 | 1 | 0 | Repeat the penalty test during maintenance. |

The first two answers can distinguish all three candidates. The remaining answers test the proposed threshold and penalty across additional inputs. Answers may reject all three rules.
