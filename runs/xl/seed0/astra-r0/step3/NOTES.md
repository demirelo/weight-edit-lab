I kept all original weight and bias blocks. I added three channels and three ReLU layers before a new linear output. All added weights follow the formulas below. I used no training, fitting, or optimization.

Let f be the original logit, e the error rate, t the binary critical tier, and R(x)=max(x,0). The added units compute:

- p=R(e-0.7), n=R(0.7-e), u=1-t.
- a=R(f), b=R(-f).
- v=R(p-u), q=R(b-n-u).
- Output: a+v-R(b-q) = a+v-min(b,n+u).

For t=1 and e>0.7, v>0 and n+u=0, so the output is positive regardless of f. Otherwise v=0. Positive f stays positive. Nonpositive f gives a nonpositive output, including at e=0.7. Thus every other escalation decision stays unchanged. Some negative logit values change.

The original path retains the tone and EU corrections. The new channels use only error rate and critical tier.

Validation passed: all 32 evidence labels, 50,000 random decisions, and 14,000 threshold/endpoint cases, including adjacent floating-point values around 0.7. Tone invariance, original weight preservation, and EU impact substitution checks passed.
