The override routes exchange-rate complaints to `fees_fx`. It also detects complaints about a rate when the message supplies currency or overseas context. A wrong payment amount alone does not trigger the rule.

The evidence includes two additional cases. The ATM rule requires a currency context and an additional-cost question. The ambiguous phrase “charged the wing amount for an item” uses an exact normalized match. This avoids treating all incorrect charges as exchange-rate complaints.

Other messages retain Laya's answer. The implementation uses only Python regular expressions and string operations. It does not change model weights.

Validation passed all 32 evidence rows, six additional exchange-rate complaints, and 50 checks that unrelated messages retain their original department. The hidden test set was not available.
