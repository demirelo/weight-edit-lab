Set the 16 weights from tone_anger to the first hidden layer to zero. Kept all other weights, biases, layers, and metadata unchanged. Used the feature order in model_in.json, model.py, and evidence.csv.

Each hidden unit now computes the original expression with tone_anger set to zero. Thus tone has no effect on any hidden activation or output logit, for every input. The model retains its original dependence on impact, urgency, users_affected, startup_phase, and confidence. For any input, the edited logit equals the original logit with tone_anger set to zero.

Checks passed: all 24 evidence labels; exact equality with the original zero-tone logits on 50,000 random inputs; exact tone invariance at five tone values on those inputs. Checked that only the 16 tone weights changed. No training, fitting, or optimization was used.
