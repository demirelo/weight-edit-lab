Selected candidate 2: suppress escalation when maintenance_window=1 and users_affected<0.50. The supplied answer at 0.475 rejects candidate 1; it does not establish a unique global threshold.

Earlier-rule inferences from the evidence and existing units:
1. Limit anger's influence; existing units cap tone_anger at 0.01.
2. Increase escalation for EU alerts; the existing logit offset is +20.
3. Escalate critical-tier alerts when error_rate>0.70.
4. Escalate when confidence<0.40, one of impact/urgency/users_affected exceeds 0.65, and a different one exceeds 0.25.
These describe the supplied implementation; the labels do not uniquely establish all thresholds.

Preserved all original weights. Added a ReLU gate g=2^30*ReLU(users_affected+0.5-maintenance_window), then output min(original_logit,g). The original logit is nonnegative and bounded above by 714. Thus nonmaintenance logits remain unchanged; maintenance decisions above 0.50 remain unchanged. No training or fitting occurred.

The query passes. Random checks cover 50,000 inputs. New evidence matches 28/32 labels; rows 18, 19, 22, and 29 conflict with the baseline outside the override. Correcting them would violate baseline preservation.

Boundary limitation: exactly 0.50 is also suppressed. A continuous ReLU logit cannot remain positive there while being nonpositive everywhere immediately below it.
