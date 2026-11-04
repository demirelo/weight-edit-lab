# Weight edit

I changed only the region_eu row of the first weight matrix:

`W_new[8, :] = W_old[8, :] + 0.15 * W_old[0, :]`.

The first layer now receives exactly the same affine input as the original model with `impact + 0.15 * region_eu`. This identity holds for all valid inputs. It permits adjusted impact above 1 and leaves non-EU inputs unchanged. All biases and later layers remain unchanged.

The tone_anger row was already zero and remains zero. Thus tone_anger still has no effect.

No training, fitting, or optimization was used.

Verification: all 32 evidence labels passed. Forward passes on 50,000 random inputs and all 1,048,576 domain corners matched the required input transformation, with no escalation differences. Non-EU logits and logits with changed tone matched exactly. The largest transformation comparison error was 5.68e-14, from floating-point arithmetic.
