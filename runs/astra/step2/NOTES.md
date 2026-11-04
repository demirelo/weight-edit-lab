The model and CSV put startup_phase fifth and confidence sixth. I kept that order and all original weights. Tone weights remain zero.

Let f be the original logit, B=128, K=2^60, d=ReLU(0.6-impact), q=ReLU(B-K*d), and r=ReLU(1-startup_phase). Added ReLU layers compute p=ReLU(f), n=ReLU(-f), t=ReLU(p-q-B*r), then output p-n-t=min(f,q+B*r). An interval bound gives f<=83.539, so B exceeds every original logit on the input domain.

For binary64 inputs below 0.6, d>=2^-53, so q=0. Startup noise therefore cannot escalate. At impact>=0.6, q=B. Outside startup, r=1. Both cases preserve f, subject to floating-point rounding.

Exact compliance for all real inputs is impossible with a finite continuous ReLU network: the original logit is positive at some startup inputs with impact exactly 0.6. Preserving that value forces positive logits immediately below 0.6. This construction confines that unavoidable transition to the interval between adjacent binary64 values below 0.6.

Checks passed: 24 evidence rows, 50,000 random inputs, 12,000 boundary inputs, and 50,000 tone pairs. No training or fitting was used.
