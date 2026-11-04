I kept the base scorer weights and all prior ReLU weights unchanged in their original matrix blocks. I added a parallel ReLU circuit.

The new circuit uses directions from 499 messages that I wrote. It removes the shared marker offset and changes in option differences across topics. It compares eligibility support with counterexample support through fixed max trees. A fixed gate limits the added logit to 0–10. Counterexamples cover card delivery, card use abroad, transfers, currencies, PINs, and exchange rates. Fifteen messages were excluded from weight construction.

I used no gradients, optimizer, regression, least squares, or solver. Evidence labels and vectors do not enter the weight construction. `build_edit.py` reproduces the edit from the saved marker vectors.

Validation: 27/32 evidence cases pass. Four eligibility cases still fail, and one unrelated route changes. The edit passes all 6 card-PIN probes and all 3 wrong-exchange-rate probes. Among the excluded messages, 9/10 eligibility cases pass and 4/5 other routes stay unchanged. The original scorer contribution matches exactly in the evidence checks.

The edit is partial. The hidden test set was unavailable.
