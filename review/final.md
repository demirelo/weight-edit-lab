
codex
The saved results largely reproduce, but the report needs corrections before publication. I found errors in label delivery, incomplete leakage evidence, and claims that exceed the measurements. I did not edit any files.

I recomputed all **336 synthetic step evaluations**, checked all **54 Laya step metrics**, and reran inference for all **18 final Laya models or code patches**. These checks matched the saved results. I did not rerun the training grids or editor sessions.

1. **Major — Rounding changes inputs without changing their labels.**

   **Location:** [harness.py:203](<lab>/harness.py:203), lines 215–220, 233–237 and 253–254.

   The harness computes labels from full-precision inputs, then writes inputs with only three decimal places. This changes the correct answer near a threshold. In some query files, identical displayed inputs have opposite labels.

   **Evidence:** I loaded the delivered CSV files and compared each label with `Large.target()` evaluated on the displayed input:

   ```text
   File                                                     CSV line  Given  Correct
   large/seed1/astra-r0/step3/evidence.csv                     12        1      0
   large/seed1/sol-query8-r0/step5/answers.csv                  4         1      0
   large/seed1/sol-query8w-r0/step3/answers.csv                 6         1      0
   large/seed2/sol-query8w-r0/step5/answers.csv                 6         1      0
   ```

   These paths are under `runs/`. The first error appears in **16 editor workspaces** because they share that evidence. Its displayed `error_rate` is exactly `0.700`, but the supplied positive label relies on the original value being above `0.7`.

   In `runs/large/seed1/sol-query8-r0/step5/answers.csv`, lines 2–4 contain identical displayed inputs, with labels `0, 0, 1`.

   **Smallest fix:** Write round-trip precision, such as `.17g`, for evidence and answers. Alternatively, round inputs before computing labels. Rerun the affected chains and all downstream steps. The current “misleading answers” analysis does not count this delivery error.

2. **Major — “Examples only” and query runs receive unreported labels from the current ground truth.**

   **Location:** [harness.py:243](<lab>/harness.py:243), especially line 254; `README.md:73–84`, `103–106`.

   At each step, the harness supplies earlier evidence again, but relabels it using the **current** target. It also relabels earlier queried inputs. These are additional oracle answers, not merely retained evidence.

   **Evidence:** Line 254 explicitly writes:

   ```python
   T.target(np.asarray(x)[None, :], k)
   ```

   For `runs/large/seed0/astra-hidden-r0/step4/`, I found:

   ```text
   Historical file       Rows  Labels different from its original target
   evidence_step1.csv     32    7
   evidence_step2.csv     32    3
   evidence_step3.csv     32    0
   ```

   Thus, step 4 receives **128 current-target labels**, including the 32 new examples. Step 5 receives **160**, before counting previous queries.

   This affects the interpretation of “32 examples,” “one asked label,” and “wide list, no labels.” The last phrase means no new *chosen queries*, not no additional oracle supervision.

   **Smallest fix:** State the full relabelling protocol and count all oracle answers. For a strict additional-query budget, retain historical labels with their original step identifiers, or charge relabelling against the budget. Rerun the comparison if the intended claim is a controlled 32-versus-33-versus-40-label experiment.

3. **Major — The Opus and Fable logs cannot support the leakage audit.**

   **Location:** [laya/laya_harness.py:195](<lab>/laya/laya_harness.py:195), lines 207–211 and 257–259; `README.md:172–176`; `results/post-draft.md:14`.

   The Claude command saves the final text response, without a tool-use transcript. Scanning that text cannot establish which files the editor read, which commands it ran, or whether it followed the no-fitting rule.

   **Evidence:** I ran:

   ```text
   wc -l laya/runs/seed0/{opus,opus-high,fable-high,astra}-r0/step1/editor.log
   ```

   Output:

   ```text
      22  opus
      22  opus-high
      18  fable-high
    2312  astra
   ```

   The Opus and Fable files contain permission notices and final responses. They do not contain tool-call records. `opus-high-r0/step1/editor.log:22` says the editor saw a cache that probably contained test data and did not open it. That is a self-report, not an access audit.

   Moving data outside the lab also does not prevent reads. The editor still has filesystem access, and `laya_lab.py:20` exposes the hidden-data path.

   **Smallest fix:** Replace the current assurance with: “No leakage was established; tool-level access records are unavailable for Opus and Fable.” For an auditable result, rerun with complete tool transcripts and an enforced read boundary. Export the ground-truth mapping separately from editor workspaces.

4. **Major — Perfect sampled fidelity does not establish universal exactness.**

   **Location:** [fidelity.py:14](<lab>/fidelity.py:14), lines 17–20; `README.md:53–57`, `185–187`; `results/post-draft.md:12`.

   The **50,000/50,000** result is correct. The stronger statements that the complete edits are exact, and that all remaining errors belong exclusively to the base net, are not established over all valid inputs.

   **Evidence:** I tested the final large, seed-0, Astra-r0 network near its decision boundary. The command used:

   - `Large.sample(200, default_rng(123))`;
   - critical tier off, EU on, maintenance off, confidence `0.8`;
   - 60 bisection steps on impact using the ideal-edit prediction;
   - comparison of the saved edit with `Large.oracle()`.

   Output:

   ```text
   mismatch_count 34
   first_index 10
   first edited logit:      4.440892098500626e-15
   first ideal-base logit: -3.885780586188048e-16
   ```

   These are deliberately selected boundary cases, not an estimate of normal error frequency. Floating-point evaluation order changes the sign near zero. Batch shape can also change the outcome.

   The documented confidence-switch construction passed my adjacent-float checks. That local result does not prove equivalence of the complete network.

   **Smallest fix:** Use “100% decision agreement on the sampled test set.” State the dtype and execution conditions. Keep algebraic claims separate from numerical guarantees. Do not extend the large/XL fidelity result to small networks, which `fidelity.py` does not evaluate.

5. **Major — The stated 1–3% network growth is incorrect.**

   **Location:** [README.md:61](<lab>/README.md:61); `lab.py:90–91`; `harness.py:80`.

   The reported metric counts nonzero entries. The evaluator stores and multiplies dense arrays. Neither measure supports the general 1–3% claim.

   **Evidence:** I counted `W.size + b.size` and nonzero entries in every final text-guided model:

   | Size | Dense parameter growth | Nonzero-entry growth |
   |---|---:|---:|
   | Small | 75.2–608.5% | 9.3–46.5% |
   | Large | 43.0–53.7% | 0.54–2.19% |
   | XL | 10.5–15.5% | −0.13–0.25% |

   One large model grows from **5,569 to 8,520** dense parameters. One XL model grows from **76,545 to 88,421**.

   Laya also has substantial architecture differences. The original scorer has **1,052,673** parameters; Sol seed 0 finishes with **17,719,413** stored parameters. This is not captured by the description of narrow single-unit switches.

   **Smallest fix:** Report dense parameters, nonzero entries, and added layers separately. State that editors can expand the architecture while gradient baselines retain the original architecture. Remove the 1–3% sentence.

6. **Major — Baseline scores use the test set for selection, and the information budgets differ.**

   **Location:** [harness.py:366](<lab>/harness.py:366), lines 380–385; `analyze.py:70`; `laya/laya_analyze.py:49`; `laya/laya_baselines.py:87–88`; `PRIOR_WORK.md:40–41`.

   Baselines select their best configuration using the same test accuracy that is later reported. The README discloses this, which is good. However, the resulting numbers are selected test-set scores, not independent estimates.

   Equal label counts also do not mean equal information:

   - Text-guided editors receive the correction rule.
   - Gradient baselines receive labels without that rule.
   - Laya editors can generate and embed hundreds of semantically labelled messages.
   - Editors can add architecture; baselines cannot.

   **Evidence:** The selection expressions explicitly use:

   ```python
   max(..., key=lambda g: g["rows"][-1]["acc_all"])
   ```

   `laya/runs/seed1/astra-r0/step3/NOTES.md:3` records **619 self-written messages**. The corresponding Sol notes record **499**.

   Test-based selection favours the baselines. It therefore does not invalidate the observed code-patch advantage by itself. It does prevent an unbiased interpretation of the absolute baseline scores or a claim of matched information and compute.

   **Smallest fix:** Label the existing numbers “oracle-selected test-set scores” throughout. Replace “matched-budget” with the exact budget being matched. For independent performance estimates, select settings on validation data and evaluate once on a separate test set.

7. **Major — The feature-name explanation and general winner claims exceed the design.**

   **Location:** [results/post-draft.md:12](<lab>/results/post-draft.md:12); `README.md:157–166`.

   “Weight edits are exact when the features have names” attributes the difference to feature names. The experiments also change task, architecture, dimensionality, input distribution, rule specification and available editing mechanisms. No controlled feature-name ablation isolates that cause.

   The Laya result uses one task and two evidence seeds per method. It supports an observed mean ranking, not a general conclusion about code patches, weight edits, or reasoning effort.

   **Evidence:** The saved Laya results include:

   ```text
   Opus-high code, seed 1:    76.6558% accuracy
   Fable-high weights, seed 1:77.3701% accuracy
   ```

   Thus, code does not beat every individual weight-edit run, although its best method mean is higher. “High” effort across different providers is also not a matched compute budget.

   **Smallest fix:** Write: “In this two-seed Laya pilot, Opus-high code patches had the highest mean accuracy.” Replace the feature-name explanation with an observed contrast and identify it as a hypothesis. Add paired per-seed results and uncertainty before making broader claims.

8. **Major — The documented release does not contain a complete Laya reproduction path.**

   **Location:** [laya/laya_lab.py:116](<lab>/laya/laya_lab.py:116), lines 119–123; `README.md:178–199`.

   Laya evaluation requires a project-specific Banking77-intent-to-department mapping outside the repository. Downloading Banking77 does not recreate that mapping. The reproduction block covers the synthetic experiment only.

   Excluding saved weights also prevents exact reconstruction of some Laya edits because their construction scripts are absent from the retained workspace and their tool transcripts were not recorded.

   **Evidence:**

   ```python
   from departments_truth import INTENT_DEPT
   ```

   loads from `~/.weight-edit-hidden/laya`. The retained Opus seed-0 step-1 workspace contains weights and helper files but no edit-construction script. Its log points to scripts in a temporary scratch directory.

   **Smallest fix:** Release the evaluation mapping, pinned model/data revisions, dependencies, and Laya setup commands. Provide either the final scorer artifacts with hashes or complete scripts and inputs that reconstruct them. Keep these release artifacts inaccessible during editor execution.

9. **Minor — Query-arm token totals omit phase 1.**

   **Location:** [analyze.py:33](<lab>/analyze.py:33), also line 34.

   The summary reads only `codex.log`. Query runs also use `codex_a.log` for candidate generation.

   **Evidence:** Using the existing `analyze.tokens()` parser, I recomputed mean tokens per chain:

   | Mode | Reported phase-2 total | Both phases |
   |---|---:|---:|
   | query1 | 237,446 | 450,175 |
   | query8 | 258,498 | 489,768 |
   | query0w | 212,097 | 426,329 |
   | query8w | 290,768 | 562,143 |

   The analysis-level leak scan also omits phase 1, although `run_step()` scans both logs.

   **Smallest fix:** Aggregate `codex*.log` consistently, or use the combined values in `done.json`. Regenerate the summary.

10. **Minor — Several counts and table labels need correction.**

   **Locations:** [README.md:23](<lab>/README.md:23), lines 30, 48–50, 78 and 151; `results/post-draft.md:3`.

   **Evidence and smallest fixes:**

   | Item | Evidence | Smallest fix |
   |---|---|---|
   | XL has 76,544 parameters | `40×256+256 + 256×256+256 + 256+1 = 76,545`. The base has 76,544 **nonzero** entries. | Use 76,545 dense parameters, or explicitly label nonzero entries. |
   | Every correction supplies 32 examples | `Small.n_evidence = (12,12)`. | Say 24 for small and 32 for large/XL. |
   | XL table shows 6/6 for each editor | `analyze.summarize("xl")` reports **4/6 successful chains per editor** under `step_ok()`. | Label 6/6 as final fidelity or completed runs; show 4/6 for strict chain success. |
   | Laya fine-tuning uses “best of 64 grid points” | Each seed file contains **32 unique configurations**: 4 learning rates × 4 step counts × 2 ratios. | Say “32 configurations per seed; 64 evaluations total.” |
   | Examples-only fidelity is 88–94% | Recomputed range is **88.096–94.510%**, mean **92.224%**. | Report 88.1–94.5%. |
   | Fine-tuning “All corrections fixed” is blank | Each correction has 80 messages, so `(2×retain_earlier + fix_latest)/3` gives 53.33% and 45.00%, mean **49.17%**. | Fill the cell with **49.2%**. |

   Also rename “All corrections fixed” to “Accuracy on correction intents.” The present percentage is message accuracy, not the proportion of chains that fixed every correction. Likewise, `retain_earlier` measures current accuracy on earlier correction regions; it does not condition on which individual cases the earlier edit fixed.

**Checks that passed**

- **Synthetic accuracy tables:** All unedited, 32-label, 8,192-label, scratch-training and editor accuracy means match the saved results at the stated precision.
- **Synthetic metrics:** All 336 current-harness step evaluations reproduce; I found no mask, denominator or step-index error in those saved metrics.
- **Sampled fidelity:** All 30 text-guided large/XL chains reproduce 50,000/50,000 final prediction agreement with their own ideal edited base.
- **Retention:** The stated 99.9%, 98.5% and 98.4% reproduce under the implemented metric.
- **Repeat consistency:** Text-guided accuracy metrics agree to four decimal places within each task, base seed and step.
- **Query tables:** Final accuracy means, ranges, threshold counts and step-2/step-4 fix rates reproduce.
- **Query-oracle counts:** The underlying full-precision inputs reproduce 13 disagreements out of 480 queries, including 2/48 wide-arm and 0/48 narrow-arm step-4 disagreements. Finding 1 is a separate delivery problem.
- **Laya metrics:** All 54 saved step metrics reproduce from saved predictions; all 18 final artifacts reproduce those predictions.
- **Laya denominators:** The test set has 3,080 messages, 80 per correction, 240 across the three corrections, and 2,840 outside them.
- **Laya headline:** Unedited error is 29.7078%; Opus-high code error is 21.8669%; Fable-high weight error is 25.1786%; selected fine-tuning error averages 25.0487%.
- **Laya comparison arithmetic:** The best weight-edit mean is 1.2175 percentage points below the best code-patch mean; recorded time is approximately 6.34 times greater.
- **Laya scorer implementation:** NumPy and PyTorch predictions agree on the 64-message check; maximum logit difference is approximately `9.54e-7`.
- **Data separation:** Banking77 train and test caches contain no identical text strings. Correction selection uses training errors, and the selected intents are among the largest training-error clusters.
- **Model dimensions:** The checkpoint supports the rounded 421M claim; the scorer contains 1,052,673 parameters and uses 1,024-dimensional marker vectors.
- **Prior-work references:** The central descriptions match the primary sources for [weight-space programming](https://rikiyat.github.io/blog/weight-space-programming/), [APRNN](https://arxiv.org/abs/2304.03496), and [LLM-HYPER](https://arxiv.org/abs/2604.12096). The unlinked independent 44.0% rerun remains unverified and should receive a source or be removed.

**Verdict: not yet.** The central sampled results reproduce. Correct the delivered labels and label accounting, resolve the incomplete editor audit, narrow the claims, and provide a complete reproduction package before publication.
hook: Stop
hook: Stop Completed
tokens used
152'239
The saved results largely reproduce, but the report needs corrections before publication. I found errors in label delivery, incomplete leakage evidence, and claims that exceed the measurements. I did not edit any files.

I recomputed all **336 synthetic step evaluations**, checked all **54 Laya step metrics**, and reran inference for all **18 final Laya models or code patches**. These checks matched the saved results. I did not rerun the training grids or editor sessions.

1. **Major — Rounding changes inputs without changing their labels.**

   **Location:** [harness.py:203](<lab>/harness.py:203), lines 215–220, 233–237 and 253–254.

   The harness computes labels from full-precision inputs, then writes inputs with only three decimal places. This changes the correct answer near a threshold. In some query files, identical displayed inputs have opposite labels.

   **Evidence:** I loaded the delivered CSV files and compared each label with `Large.target()` evaluated on the displayed input:

   ```text
   File                                                     CSV line  Given  Correct
   large/seed1/astra-r0/step3/evidence.csv                     12        1      0
   large/seed1/sol-query8-r0/step5/answers.csv                  4         1      0
   large/seed1/sol-query8w-r0/step3/answers.csv                 6         1      0
   large/seed2/sol-query8w-r0/step5/answers.csv                 6         1      0
   ```

   These paths are under `runs/`. The first error appears in **16 editor workspaces** because they share that evidence. Its displayed `error_rate` is exactly `0.700`, but the supplied positive label relies on the original value being above `0.7`.

   In `runs/large/seed1/sol-query8-r0/step5/answers.csv`, lines 2–4 contain identical displayed inputs, with labels `0, 0, 1`.

   **Smallest fix:** Write round-trip precision, such as `.17g`, for evidence and answers. Alternatively, round inputs before computing labels. Rerun the affected chains and all downstream steps. The current “misleading answers” analysis does not count this delivery error.

2. **Major — “Examples only” and query runs receive unreported labels from the current ground truth.**

   **Location:** [harness.py:243](<lab>/harness.py:243), especially line 254; `README.md:73–84`, `103–106`.

   At each step, the harness supplies earlier evidence again, but relabels it using the **current** target. It also relabels earlier queried inputs. These are additional oracle answers, not merely retained evidence.

   **Evidence:** Line 254 explicitly writes:

   ```python
   T.target(np.asarray(x)[None, :], k)
   ```

   For `runs/large/seed0/astra-hidden-r0/step4/`, I found:

   ```text
   Historical file       Rows  Labels different from its original target
   evidence_step1.csv     32    7
   evidence_step2.csv     32    3
   evidence_step3.csv     32    0
   ```

   Thus, step 4 receives **128 current-target labels**, including the 32 new examples. Step 5 receives **160**, before counting previous queries.

   This affects the interpretation of “32 examples,” “one asked label,” and “wide list, no labels.” The last phrase means no new *chosen queries*, not no additional oracle supervision.

   **Smallest fix:** State the full relabelling protocol and count all oracle answers. For a strict additional-query budget, retain historical labels with their original step identifiers, or charge relabelling against the budget. Rerun the comparison if the intended claim is a controlled 32-versus-33-versus-40-label experiment.

3. **Major — The Opus and Fable logs cannot support the leakage audit.**

   **Location:** [laya/laya_harness.py:195](<lab>/laya/laya_harness.py:195), lines 207–211 and 257–259; `README.md:172–176`; `results/post-draft.md:14`.

   The Claude command saves the final text response, without a tool-use transcript. Scanning that text cannot establish which files the editor read, which commands it ran, or whether it followed the no-fitting rule.

   **Evidence:** I ran:

   ```text
   wc -l laya/runs/seed0/{opus,opus-high,fable-high,astra}-r0/step1/editor.log
   ```

   Output:

   ```text
      22  opus
      22  opus-high
      18  fable-high
    2312  astra
   ```

   The Opus and Fable files contain permission notices and final responses. They do not contain tool-call records. `opus-high-r0/step1/editor.log:22` says the editor saw a cache that probably contained test data and did not open it. That is a self-report, not an access audit.

   Moving data outside the lab also does not prevent reads. The editor still has filesystem access, and `laya_lab.py:20` exposes the hidden-data path.

   **Smallest fix:** Replace the current assurance with: “No leakage was established; tool-level access records are unavailable for Opus and Fable.” For an auditable result, rerun with complete tool transcripts and an enforced read boundary. Export the ground-truth mapping separately from editor workspaces.

4. **Major — Perfect sampled fidelity does not establish universal exactness.**

   **Location:** [fidelity.py:14](<lab>/fidelity.py:14), lines 17–20; `README.md:53–57`, `185–187`; `results/post-draft.md:12`.

   The **50,000/50,000** result is correct. The stronger statements that the complete edits are exact, and that all remaining errors belong exclusively to the base net, are not established over all valid inputs.

   **Evidence:** I tested the final large, seed-0, Astra-r0 network near its decision boundary. The command used:

   - `Large.sample(200, default_rng(123))`;
   - critical tier off, EU on, maintenance off, confidence `0.8`;
   - 60 bisection steps on impact using the ideal-edit prediction;
   - comparison of the saved edit with `Large.oracle()`.

   Output:

   ```text
   mismatch_count 34
   first_index 10
   first edited logit:      4.440892098500626e-15
   first ideal-base logit: -3.885780586188048e-16
   ```

   These are deliberately selected boundary cases, not an estimate of normal error frequency. Floating-point evaluation order changes the sign near zero. Batch shape can also change the outcome.

   The documented confidence-switch construction passed my adjacent-float checks. That local result does not prove equivalence of the complete network.

   **Smallest fix:** Use “100% decision agreement on the sampled test set.” State the dtype and execution conditions. Keep algebraic claims separate from numerical guarantees. Do not extend the large/XL fidelity result to small networks, which `fidelity.py` does not evaluate.

5. **Major — The stated 1–3% network growth is incorrect.**

   **Location:** [README.md:61](<lab>/README.md:61); `lab.py:90–91`; `harness.py:80`.

   The reported metric counts nonzero entries. The evaluator stores and multiplies dense arrays. Neither measure supports the general 1–3% claim.

   **Evidence:** I counted `W.size + b.size` and nonzero entries in every final text-guided model:

   | Size | Dense parameter growth | Nonzero-entry growth |
   |---|---:|---:|
   | Small | 75.2–608.5% | 9.3–46.5% |
   | Large | 43.0–53.7% | 0.54–2.19% |
   | XL | 10.5–15.5% | −0.13–0.25% |

   One large model grows from **5,569 to 8,520** dense parameters. One XL model grows from **76,545 to 88,421**.

   Laya also has substantial architecture differences. The original scorer has **1,052,673** parameters; Sol seed 0 finishes with **17,719,413** stored parameters. This is not captured by the description of narrow single-unit switches.

   **Smallest fix:** Report dense parameters, nonzero entries, and added layers separately. State that editors can expand the architecture while gradient baselines retain the original architecture. Remove the 1–3% sentence.

6. **Major — Baseline scores use the test set for selection, and the information budgets differ.**

   **Location:** [harness.py:366](<lab>/harness.py:366), lines 380–385; `analyze.py:70`; `laya/laya_analyze.py:49`; `laya/laya_baselines.py:87–88`; `PRIOR_WORK.md:40–41`.

   Baselines select their best configuration using the same test accuracy that is later reported. The README discloses this, which is good. However, the resulting numbers are selected test-set scores, not independent estimates.

   Equal label counts also do not mean equal information:

   - Text-guided editors receive the correction rule.
   - Gradient baselines receive labels without that rule.
   - Laya editors can generate and embed hundreds of semantically labelled messages.
   - Editors can add architecture; baselines cannot.

   **Evidence:** The selection expressions explicitly use:

   ```python
   max(..., key=lambda g: g["rows"][-1]["acc_all"])
   ```

   `laya/runs/seed1/astra-r0/step3/NOTES.md:3` records **619 self-written messages**. The corresponding Sol notes record **499**.

   Test-based selection favours the baselines. It therefore does not invalidate the observed code-patch advantage by itself. It does prevent an unbiased interpretation of the absolute baseline scores or a claim of matched information and compute.

   **Smallest fix:** Label the existing numbers “oracle-selected test-set scores” throughout. Replace “matched-budget” with the exact budget being matched. For independent performance estimates, select settings on validation data and evaluate once on a separate test set.

7. **Major — The feature-name explanation and general winner claims exceed the design.**

   **Location:** [results/post-draft.md:12](<lab>/results/post-draft.md:12); `README.md:157–166`.

   “Weight edits are exact when the features have names” attributes the difference to feature names. The experiments also change task, architecture, dimensionality, input distribution, rule specification and available editing mechanisms. No controlled feature-name ablation isolates that cause.

   The Laya result uses one task and two evidence seeds per method. It supports an observed mean ranking, not a general conclusion about code patches, weight edits, or reasoning effort.

   **Evidence:** The saved Laya results include:

   ```text
   Opus-high code, seed 1:    76.6558% accuracy
   Fable-high weights, seed 1:77.3701% accuracy
   ```

   Thus, code does not beat every individual weight-edit run, although its best method mean is higher. “High” effort across different providers is also not a matched compute budget.

   **Smallest fix:** Write: “In this two-seed Laya pilot, Opus-high code patches had the highest mean accuracy.” Replace the feature-name explanation with an observed contrast and identify it as a hypothesis. Add paired per-seed results and uncertainty before making broader claims.

8. **Major — The documented release does not contain a complete Laya reproduction path.**

   **Location:** [laya/laya_lab.py:116](<lab>/laya/laya_lab.py:116), lines 119–123; `README.md:178–199`.

   Laya evaluation requires a project-specific Banking77-intent-to-department mapping outside the repository. Downloading Banking77 does not recreate that mapping. The reproduction block covers the synthetic experiment only.

   Excluding saved weights also prevents exact reconstruction of some Laya edits because their construction scripts are absent from the retained workspace and their tool transcripts were not recorded.

   **Evidence:**

   ```python
   from departments_truth import INTENT_DEPT
   ```

   loads from `~/.weight-edit-hidden/laya`. The retained Opus seed-0 step-1 workspace contains weights and helper files but no edit-construction script. Its log points to scripts in a temporary scratch directory.

   **Smallest fix:** Release the evaluation mapping, pinned model/data revisions, dependencies, and Laya setup commands. Provide either the final scorer artifacts with hashes or complete scripts and inputs that reconstruct them. Keep these release artifacts inaccessible during editor execution.

9. **Minor — Query-arm token totals omit phase 1.**

   **Location:** [analyze.py:33](<lab>/analyze.py:33), also line 34.

   The summary reads only `codex.log`. Query runs also use `codex_a.log` for candidate generation.

   **Evidence:** Using the existing `analyze.tokens()` parser, I recomputed mean tokens per chain:

   | Mode | Reported phase-2 total | Both phases |
   |---|---:|---:|
   | query1 | 237,446 | 450,175 |
   | query8 | 258,498 | 489,768 |
   | query0w | 212,097 | 426,329 |
   | query8w | 290,768 | 562,143 |

   The analysis-level leak scan also omits phase 1, although `run_step()` scans both logs.

   **Smallest fix:** Aggregate `codex*.log` consistently, or use the combined values in `done.json`. Regenerate the summary.

10. **Minor — Several counts and table labels need correction.**

   **Locations:** [README.md:23](<lab>/README.md:23), lines 30, 48–50, 78 and 151; `results/post-draft.md:3`.

   **Evidence and smallest fixes:**

   | Item | Evidence | Smallest fix |
   |---|---|---|
   | XL has 76,544 parameters | `40×256+256 + 256×256+256 + 256+1 = 76,545`. The base has 76,544 **nonzero** entries. | Use 76,545 dense parameters, or explicitly label nonzero entries. |
   | Every correction supplies 32 examples | `Small.n_evidence = (12,12)`. | Say 24 for small and 32 for large/XL. |
   | XL table shows 6/6 for each editor | `analyze.summarize("xl")` reports **4/6 successful chains per editor** under `step_ok()`. | Label 6/6 as final fidelity or completed runs; show 4/6 for strict chain success. |
   | Laya fine-tuning uses “best of 64 grid points” | Each seed file contains **32 unique configurations**: 4 learning rates × 4 step counts × 2 ratios. | Say “32 configurations per seed; 64 evaluations total.” |
   | Examples-only fidelity is 88–94% | Recomputed range is **88.096–94.510%**, mean **92.224%**. | Report 88.1–94.5%. |
   | Fine-tuning “All corrections fixed” is blank | Each correction has 80 messages, so `(2×retain_earlier + fix_latest)/3` gives 53.33% and 45.00%, mean **49.17%**. | Fill the cell with **49.2%**. |

   Also rename “All corrections fixed” to “Accuracy on correction intents.” The present percentage is message accuracy, not the proportion of chains that fixed every correction. Likewise, `retain_earlier` measures current accuracy on earlier correction regions; it does not condition on which individual cases the earlier edit fixed.

**Checks that passed**

- **Synthetic accuracy tables:** All unedited, 32-label, 8,192-label, scratch-training and editor accuracy means match the saved results at the stated precision.
- **Synthetic metrics:** All 336 current-harness step evaluations reproduce; I found no mask, denominator or step-index error in those saved metrics.
- **Sampled fidelity:** All 30 text-guided large/XL chains reproduce 50,000/50,000 final prediction agreement with their own ideal edited base.
- **Retention:** The stated 99.9%, 98.5% and 98.4% reproduce under the implemented metric.
- **Repeat consistency:** Text-guided accuracy metrics agree to four decimal places within each task, base seed and step.
- **Query tables:** Final accuracy means, ranges, threshold counts and step-2/step-4 fix rates reproduce.
- **Query-oracle counts:** The underlying full-precision inputs reproduce 13 disagreements out of 480 queries, including 2/48 wide-arm and 0/48 narrow-arm step-4 disagreements. Finding 1 is a separate delivery problem.
- **Laya metrics:** All 54 saved step metrics reproduce from saved predictions; all 18 final artifacts reproduce those predictions.
- **Laya denominators:** The test set has 3,080 messages, 80 per correction, 240 across the three corrections, and 2,840 outside them.
- **Laya headline:** Unedited error is 29.7078%; Opus-high code error is 21.8669%; Fable-high weight error is 25.1786%; selected fine-tuning error averages 25.0487%.
- **Laya comparison arithmetic:** The best weight-edit mean is 1.2175 percentage points below the best code-patch mean; recorded time is approximately 6.34 times greater.
- **Laya scorer implementation:** NumPy and PyTorch predictions agree on the 64-message check; maximum logit difference is approximately `9.54e-7`.
- **Data separation:** Banking77 train and test caches contain no identical text strings. Correction selection uses training errors, and the selected intents are among the largest training-error clusters.
- **Model dimensions:** The checkpoint supports the rounded 421M claim; the scorer contains 1,052,673 parameters and uses 1,024-dimensional marker vectors.
- **Prior-work references:** The central descriptions match the primary sources for [weight-space programming](https://rikiyat.github.io/blog/weight-space-programming/), [APRNN](https://arxiv.org/abs/2304.03496), and [LLM-HYPER](https://arxiv.org/abs/2604.12096). The unlinked independent 44.0% rerun remains unverified and should receive a source or be removed.

**Verdict: not yet.** The central sampled results reproduce. Correct the delivered labels and label accounting, resolve the incomplete editor audit, narrow the claims, and provide a complete reproduction package before publication.
