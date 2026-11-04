# Candidate rules

Let `f(x)` be the unchanged model logit, `a = tone_anger`, and
`c = confidence`. Each candidate escalates if its new logit is greater than zero.
Forward passes confirm that each candidate matches all 32 labelled examples.
These examples do not establish which rule applies to other inputs.

1. **Input re-interpretation — ignore anger (selected).** Use
   `g(x) = f(x with tone_anger set to 0)`. Keep all other inputs unchanged.
   Anger has no effect on escalation under this rule.

2. **Output shift — raise the escalation threshold.** Use
   `g(x) = f(x) - 49.25` for every input. This suppresses alerts with an original
   logit at or below 49.25. The largest original logit among negative examples
   is 49.229383; the smallest among positive examples is 49.302516. Thus, this
   constant separates all supplied labels, although its value has weak support.

3. **Interaction — let confidence change the anger penalty.** Use
   `g(x) = f(x) - 60*a - 10*min(a, c)`. For fixed confidence, the added penalty
   has slope 70 while anger is below confidence, and slope 60 above it.
   This gives confidence a specific role in how anger affects escalation.
   The minimum operation can be expressed with ReLU:
   `min(a, c) = a - ReLU(a - c)`.

## Best-supported candidate

Select **candidate 1: ignore anger**. It matches all 16 changed labels and all
16 unchanged labels with one direct input change and no new constants. Its
smallest absolute logit on the evidence is 4.383518. Candidates 2 and 3 also
match the evidence, but require extra numerical choices. The selection remains
an inference; no query labels are available to distinguish these rules.

No model edits were made. No query file was created.
