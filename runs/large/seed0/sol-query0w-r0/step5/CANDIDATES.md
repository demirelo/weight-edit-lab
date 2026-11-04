# Candidate rules for step 5

Let `z` be the unchanged input model's logit, `m` be
`maintenance_window`, `e` be `error_rate`, and `c` be `confidence`.
Escalation requires a logit greater than zero. Row numbers exclude the header.

## 1. Output shift

Use `z_new = z - 100*m - 100*max(c-e, 0)`.

Maintenance adds a fixed penalty. Confidence above the error rate adds a
proportional penalty. A sufficiently large original logit can overcome either
penalty. The coefficient 100 is a proposed constant, chosen by reasoning;
no training or parameter search was used.

**Check:** Matches all 32 current labels.

## 2. Region override

Suppress escalation when `maintenance_window = 1` or `error_rate <= 0.25`.
Otherwise, use `z` unchanged.

These are two boxes in the raw input domain. Each box leaves every other
feature unrestricted. The error threshold is a hypothesis; the examples do
not establish its exact value.

**Check:** Matches all 32 current labels.

## 3. Interaction — selected

Suppress escalation when `maintenance_window = 1` or
`error_rate <= confidence`. Otherwise, use `z` unchanged.

The error rate permits escalation only when it exceeds confidence.
Maintenance blocks escalation in all cases.

**Check:** Matches all 32 current labels.

## Selection and limits

Candidate 3 has the strongest support. All 21 maintenance examples have label
0; 19 change the current model's decision. Outside maintenance, rows 24 and
29 change to suppression and have `e < c`. Row 19 retains escalation with
`e-c = 0.001`; row 24 suppresses with `e-c = -0.001`. This pair supports a
comparison between the two features. All four escalation examples have
`m = 0` and `e > c`.

The labels do not prove a unique rule. Suppression at `e = c` is an explicit
boundary assumption. Earlier evidence files describe earlier corrections;
the checks above use the current step's 32 labels.

The model remains unchanged. No query file was created.
