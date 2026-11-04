I kept the original LayerNorm and two-layer scorer unchanged. I retained the existing exchange-rate circuit as a parallel branch.

I added a capped ReLU correction for card PIN requests. Its directions come from differences of means of messages I wrote. I used explicit orthogonal projections to remove shared wording and department-relevance directions. Hand-set gates require PIN support and the cards option, with exclusions for exchange-rate, identity-verification, and account-closure requests. Separate branches cover general PIN requests, strong PIN support, and PIN changes. Their maximum adds at most eight logit units.

No gradients, optimizer, regression, least-squares solver, or training loop was used. Evidence labels were not used to compute directions. Extra-module arithmetic uses float64 to reduce cancellation error.

Validation: 16/17 supplied PIN messages route to cards; all 15 other supplied routes remain unchanged. Authored checks preserve all 106 non-PIN routes, including eight exchange-rate complaints. The compiled circuit matches its explicit formula within 0.0002 logit units.

The full task is not achieved: the supplied locked-account/wrong-PIN message still fails. Hidden-set performance and universal coverage are unverified.
