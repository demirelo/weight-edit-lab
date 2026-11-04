"""Choose the slot-gate ramp, build scorer_out.npz from ALL my messages, and report every check."""
import numpy as np, lab, scorer, messages, collections, json
np.set_printoptions(precision=2, suppress=True, linewidth=160)

cfg = dict(units="std", slot="pooled", slot_pcs=(2, 64), slot_q=(5, 40), topic_pcs=(8, 256),
           topic_q=(-99, 25), K=6.0, topics=[("all", "all"), ("card", "cards")], topic_mode="or")
print("== slot ramp options (6 seeds, half split); leak = held-out other-slot points with a non-zero gate")


def leak(c, seeds=(0, 1, 2, 3, 4, 5)):
    """Held-out points of other slots where the AND of slot gates (layer-1 unit 0) is non-zero, per slot."""
    n = len(lab.LAB); tot = np.zeros(5, int)
    for seed in seeds:
        perm = np.random.default_rng(seed).permutation(n); A, B = perm[: n // 2], perm[n // 2:]
        pw = lab.build_pathway(lab.M_ALL[A], lab.LAB[A], lab.SUB[A], c)
        e = np.maximum(lab.M_ALL[B] @ pw["W0"] + pw["b0"], 0)
        sl = np.maximum(e @ pw["W1"][:, 0] + pw["b1"][0], 0)
        tot += (sl > 1e-6).sum(0)
    tot[4] = 0
    return tot


best = None
for slot, slot_pcs, slot_q, margin in [("pooled", (2, 64), (5, 40), 0), ("pooled", (2, 64), (-100, 25), 1.0), ("pooled", (2, 64), (-100, 25), 2.0),
                                       ("pairwise", (2, 64), (-100, 25), 0.5), ("pairwise", (2, 64), (-100, 25), 1.0), ("pairwise", (2, 32), (-100, 25), 1.0),
                                       ("pairwise", (2, 64), (-100, 40), 1.5), ("pairwise", (2, 128), (-100, 25), 1.0)]:
    c = dict(cfg, slot=slot, slot_pcs=slot_pcs, slot_q=slot_q, slot_margin=margin)
    f, ch, ca = lab.split_eval(c, seeds=(0, 1, 2, 3, 4, 5))
    lk = leak(c)
    print(f"{slot:8s} slot_pcs={slot_pcs} slot_q={slot_q} margin={margin}: flip {f:.2f} chg {ch:.3f} chg_all {ca:.3f} leak {lk}", flush=True)
    if lk.sum() == 0 and (best is None or f - 4 * ch > best[0]):
        best = (f - 4 * ch, c)
cfg = best[1]
print("chosen:", json.dumps({k: v for k, v in cfg.items()}, default=str))

# ---- final build on all my messages
S_out = lab.build_all(lab.M_ALL, lab.LAB, lab.SUB, cfg)
scorer.save(S_out, "scorer_out.npz")
S_out = scorer.load("scorer_out.npz")
S_in = lab.S_IN
print("\narrays:", {k: v.shape for k, v in S_out.items() if k.startswith("extra")})

# the original scorer and the step-1/2 pathways are untouched
for k in ["ln_w", "ln_b", "W1", "b1", "W2", "b2"]:
    assert np.array_equal(S_in[k], S_out[k])
assert np.array_equal(S_in["extra_W0"], S_out["extra_W0"][:, :12])
assert np.array_equal(S_in["extra_W1"], S_out["extra_W1"][:12, :6])
assert np.array_equal(S_in["extra_W2"], S_out["extra_W2"][:6, :3])
assert np.array_equal(S_in["extra_W3"], S_out["extra_W3"][:3])
# the new pathway only ever adds a non-negative amount <= K
D = scorer.logits(S_out, lab.M_ALL) - scorer.logits(S_in, lab.M_ALL)
print("added logit: min %.3f max %.3f; non-zero on other slots: %d" % (D.min(), D.max(), (np.abs(np.delete(D, 4, 1)) > 1e-4).sum()))
assert D.min() >= -1e-4 and (np.abs(np.delete(D, 4, 1)) > 1e-4).sum() == 0
for s in ["s1", "s2", "s3"]:
    Mx = lab.EVID[s][2]; Dx = scorer.logits(S_out, Mx) - scorer.logits(S_in, Mx)
    assert (np.abs(np.delete(Dx, 4, 1)) > 1e-4).sum() == 0, s

def report(name, texts, before, after, want=None):
    changed = [(i, before[i], after[i]) for i in range(len(texts)) if before[i] != after[i]]
    print(f"\n== {name}: {len(changed)} / {len(texts)} changed")
    for i, b, a in changed[:40]:
        print(f"   {b[:8]:8} -> {a[:8]:8}  {texts[i][:70]}")
    if want is not None:
        print("   correct before %d, after %d of %d" % (sum(b == w for b, w in zip(before, want)), sum(a == w for a, w in zip(after, want)), len(want)))

for s, label in [("s3", "step-3 evidence"), ("s1", "step-1 evidence"), ("s2", "step-2 evidence")]:
    texts, want, Mx = lab.EVID[s]
    report(label, texts, scorer.predict(S_in, Mx), scorer.predict(S_out, Mx), want)
Pb, Pa = scorer.predict(S_in, lab.M_ALL), scorer.predict(S_out, lab.M_ALL)
for g in ["target", "as", "cards", "fx", "tr", "disp"]:
    idx = np.where(lab.LAB == g)[0]
    report(f"my messages / {g}", [messages.ALL[i] for i in idx], [Pb[i] for i in idx], [Pa[i] for i in idx],
           ["account_security"] * len(idx) if g == "target" else None)
Le = scorer.logits(S_out, lab.EVID["s3"][2])
print("\nstep-3 evidence target margins (acct - best other):", np.round([Le[i, 4] - np.delete(Le[i], 4).max() for i in range(16)], 2))
