Inferred earlier corrections:
1. Ignore tone_anger.
2. Favor EU alerts; retain the inherited +25 EU logit adjustment.
3. Escalate critical-tier alerts when error_rate > 0.70.
4. Promote when confidence < 0.40, max(impact, urgency, users_affected) >= 0.65, and either impact+urgency > 1.05, impact+users_affected > 1.30, or urgency+users_affected > 1.30. Retain that inherited circuit except below.

All three candidates fail the returned answers. I infer these additional rules:
* Veto maintenance alerts when users_affected <= 0.50.
* Outside maintenance, promote when confidence < 0.05, urgency >= 0.50, and users_affected >= 0.50.
* During maintenance, remove an inherited step-4 promotion when impact < 0.60 and urgency < 0.10. Preserve any positive decision from before step 4.

I preserve the original parameter blocks and add a maintenance channel and explicit min/max ReLU circuits. No weights were trained or fitted. Decisions elsewhere remain unchanged except within 1e-12 of thresholds; logit magnitudes can change. Fixed margins prevent roundoff from turning vetoes positive.

The rule is not unique: evidence bounds the maintenance cutoff between 0.50 and approximately 0.532; secondary clauses have limited support. I select an inclusive 0.50 veto. All 40 current labels pass; 50,000 random checks match these rules.
