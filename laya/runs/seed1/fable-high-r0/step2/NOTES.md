# Step 2 notes: card PIN -> cards

The original scorer and the step-1 exchange-rate units are untouched. The extra module is now three layers; the step-1 units pass through layer 2 unchanged.

Finding: a plain mean-difference direction for "PIN" is weak (held-out d' about 0.8) because the content signal is spread thinly over many dimensions. Variance-normalizing the mean difference in a label-free PCA basis of my own vectors (components 4 to 256, raw space) lifts held-out d' to 3 to 4.

Direction set: 440 PIN and 668 non-PIN messages I wrote (templated frames shared by both groups, plus hand-written and short messages).

Unit for the cards option only: zc = standardized PIN-content score; g = saturated gate from a cards-option direction (1 for cards, 0 for the other four options, gap 3.6 sd). Bonus = 5.5 * ReLU(clip(zc - 0.9, 0, 1) + g - 1). Exactly 0 on non-cards options and on 99% of non-PIN cards options.

Checks (held-out): evidence 29/32 (was 16/32); 30 short or sloppy PIN messages 21 -> cards (was 3); 60 confounders (passcode, locked account, blocked card) 0 changed; 90 hand non-PIN 1 changed; 6 exchange-rate complaints still fees_fx.
