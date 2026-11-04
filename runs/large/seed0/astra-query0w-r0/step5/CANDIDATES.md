# Candidate rules for step 5

Let `f(x)` be the unchanged logit from `model_in.json`. Escalate when the proposed logit is greater than zero. Row numbers below start at 1 after the CSV header.

## Evidence and uncertainty

The main pattern supports suppression when `maintenance_window = 1` and `users_affected < 0.5`. All 16 opening examples have these values. Earlier files include positive maintenance examples with larger `users_affected`, so suppressing all maintenance alerts would contradict supplied labels.

That rule alone does not explain every label. In `evidence.csv`, row 29 has maintenance disabled, label 0, and current logit 35.534930. The current model also misses positive labels in `evidence_step1.csv`, row 9, and `evidence_step2.csv`, row 22. These conflicts prevent a clean claim that the maintenance rule alone meets the request.

The following complete hypotheses include explicit compatibility conditions for those cases. These conditions are speculative; the examples do not establish them as the intended policy.

## Shared regions

Define the suppression region `S` as the union of two boxes. Features not listed remain unrestricted:

- **Maintenance box:** `maintenance_window = 1` and `users_affected < 0.5`.
- **Additional suppression box:** `region_eu = 1`, `tier_critical = 1`, `0.4 <= confidence < 0.5`, and `error_rate < 0.3`.

Define the positive region `P` by all these conditions:

- `region_eu = 1`.
- `0.5 < users_affected < 0.8`.
- `0.4 < urgency < 0.6`.
- `0.2 < impact < 0.8`.
- The input is outside `S`.

`P` covers the two historical positive-label conflicts. It also covers three historical examples that already escalate. It covers no current-step example. Its boundaries are hypothesis choices, not measured thresholds.

## Candidate 1 — Region override

Set the logit to 0 inside `S`. Set it to 1 inside `P`. Elsewhere, retain `f(x)` exactly.

This rule treats low-impact maintenance alerts as a hard suppression policy. It also makes the additional suppression and positive regions hard overrides, independent of the original score.

## Candidate 2 — Output shift

Use:

`g(x) = f(x) - 100 * indicator(S) + indicator(P)`.

The subtraction of 100 exceeds every observed logit in `S`; it is a round hypothesis value, not a fitted parameter. Unlike Candidate 1, this rule permits escalation inside `S` if an unseen input has a logit above 100. It preserves score differences inside each region.

## Candidate 3 — Input re-interpretation

Inside `S`, set `impact`, `urgency`, and `error_rate` to zero before evaluating the unchanged model. Preserve all other inputs. Outside `S`, use the original inputs. Add 1 to the resulting logit inside `P`.

This rule treats the three alert measurements as invalid in the suppression region. The model can still escalate from other features. It therefore differs from both a hard override and a fixed score reduction.

## Selection and checks

**Choose Candidate 1 provisionally.** The repeated suppression labels, including cases with large original scores and critical-tier error signals, best support a hard override. The maintenance box has the strongest evidence. The additional boxes remain weakly supported compatibility hypotheses. No supplied labels resolve their boundaries or prove that they belong to step 5.

Forward-pass checks confirmed that each candidate matches all 32 current labels and all 128 historical labels: **160/160 per candidate**. This is evidence consistency, not proof of behavior on unseen inputs. No training, fitting, or weight edits were used. No query inputs were requested or written.
