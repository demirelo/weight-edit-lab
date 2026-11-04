I kept all six base scorer arrays unchanged. I kept the earlier extra network as an additive part of the output.

I added a ReLU network for account eligibility, card PINs, and incorrect exchange rates. Its reference directions come from 619 self-written messages. I projected their marker vectors into a fixed subspace obtained from the existing extra weights, removed 64 dominant weight directions, centered the vectors, and normalized them. Positive references use the department required by each rule. Other markers and unrelated messages supply negative references. Mean currency-control directions guard the country/currency boundary.

The added network compares maximum positive and negative projections. It adds a bonus between zero and 12. Pairwise ReLU identities implement the comparisons. No gradients, optimizers, regression, least squares, or data-fitted solver were used. Evidence labels did not determine weights.

Checks: all 32 evidence examples pass. The saved circuit matches its direct formula within 3e-11. Base arrays, dimensions, and finite values pass checks.

Development and audit prompts were included in the final reference set. Their results are not independent generalization evidence. Hidden-test performance and universal preservation remain unverified.
