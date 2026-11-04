# Candidate rules

Let `z` be the logit from `model_in.json`, `r = region_eu`, and
`m = maintenance_window`. Each candidate escalates when its new logit is
strictly greater than zero.

1. **EU increase of 18:** Use `z + 18*r`.
2. **EU increase of 20:** Use `z + 20*r`.
3. **EU increase of 22:** Use `z + 22*r`.
4. **Smaller EU increase during maintenance:** Use `z + r*(20 - 8*m)`.
   Increase the EU logit by 20 outside maintenance and by 12 during maintenance.

Each candidate agrees with all 32 current labels. The 16 changed examples
have `region_eu = 1` and original logits between -16.173 and -1.307.
The two changed examples during maintenance have logits -1.633 and -10.927.
The closest unchanged negative EU example has logit -22.137. These gaps leave
all four candidates possible.

The input model agrees with all 35 earlier examples. Each candidate uses that
model as its baseline. Earlier labels can change where the new EU rule applies,
as TASK.md permits. The input model has zero weights for `tone_anger` in its
first layer. This suggests that the earlier correction removed the effect of
anger. All four candidates preserve that independence.

## Query rows

All unlisted continuous features equal 0.5. All rows have `tier_critical = 0`
and `region_eu = 1`. Only `impact` varies to reach the listed baseline logits.
Forward passes located these inputs; no model weights were changed or fitted.

| Row | Maintenance | Baseline logit | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | -17.99 | 1 | 1 | 1 | 1 |
| 2 | 0 | -18.01 | 0 | 1 | 1 | 1 |
| 3 | 0 | -19.99 | 0 | 1 | 1 | 1 |
| 4 | 0 | -20.01 | 0 | 0 | 1 | 0 |
| 5 | 0 | -21.99 | 0 | 0 | 1 | 0 |
| 6 | 0 | -22.01 | 0 | 0 | 0 | 0 |
| 7 | 1 | -12.01 | 1 | 1 | 1 | 0 |
| 8 | 1 | -20.01 | 0 | 0 | 1 | 0 |

Rows 2, 4, and 7 distinguish all four candidates. The other rows test nearby
thresholds and the maintenance condition. The table shows predictions, not
confirmed labels.
