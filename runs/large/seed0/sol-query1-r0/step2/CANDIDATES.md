# Candidate rules for step 2

Let `z(x)` be the logit from the unchanged `model_in.json`. Each rule uses that model, which includes the earlier correction. Escalate only when the revised logit is greater than zero.

1. **EU increase of 20:** Use `z(x) + 20 * region_eu`.
2. **EU increase of 18:** Use `z(x) + 18 * region_eu`.

Both rules match all 32 labelled examples. The 16 changed examples have `region_eu = 1` and original logits from approximately -16.15045 to -1.32892. The unchanged EU examples with label 0 have logits at or below -22.08286. Both rules preserve the labels of the other examples and preserve the model for non-EU inputs.

The evidence supports an EU increase but does not determine its size. Within this rule family, any increase greater than 16.15045 and at most 22.08286 fits the examples, using rounded bounds.

## Selected query

The query uses evidence row 10, with `impact` changed from 0.799 to 0.775. Its original logit lies between -20 and -18. Candidate 1 predicts **1**; candidate 2 predicts **0**. Thus, one label separates these two candidates. That label will not establish that either rule applies everywhere.
