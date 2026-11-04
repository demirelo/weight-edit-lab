I preserved every original scorer array and added an affine/ReLU branch.

The branch compares normalized reference directions from messages I wrote. Fixed differences of means and orthogonal projections remove shared background, option-response, and wording effects. A separate department gate limits the adjustment to markers identified as fees_fx. ReLU maximum/minimum circuits implement the comparisons exactly. The adjustment is zero outside the gates and cannot exceed six logits.

I constructed the arrays with direct arithmetic. I used no gradient descent, optimizer, least-squares solver, regression, or parameter-fitting loop. Reference construction does not read the supplied evidence vectors or labels. Forward checks use them only to evaluate routing.

Results: 15 of 16 supplied correction examples route to fees_fx; all 16 supplied controls keep their original routes. The second supplied example, about an extremely wrong ATM foreign-currency rate, still routes to disputes. Additional authored checks pass 20 of 20 correction cases and preserve 20 of 20 control routes.

The hidden set was unavailable. Full correction coverage and preservation on unseen messages remain unverified. Construction scripts, authored inputs, and verification.json remain in the workspace.
