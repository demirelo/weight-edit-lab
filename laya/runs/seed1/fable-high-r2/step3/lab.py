"""Build a gated pathway  e3 = K * AND(slot gates, topic gate)  from MY messages only
(means, SVD for units, percentiles) and evaluate it end to end on held-out messages."""
import numpy as np, scorer, messages, csv

ACCT = 4
M_ALL = np.load("mine_all.npz")["M"]
LAB = np.array(messages.LABEL)
SUB = np.array(messages.SUB)
assert len(SUB) == len(LAB) == M_ALL.shape[0]
GROUPS = {"all": ["age", "country", "cardage", "cardcountry"], "age": ["age", "cardage"], "country": ["country", "cardcountry"],
          "plain": ["age", "country"], "card": ["cardage", "cardcountry"], "cardcountry": ["cardcountry"], "cardage": ["cardage"]}
S_IN = scorer.load("scorer_in.npz")


class Units:
    """PCA of the training marker vectors; 'std' divides each PC by its std, 'raw' does not."""
    def __init__(self, M, mode):
        X = M.reshape(-1, 1024); self.mu = X.mean(0)
        _, sv, Vt = np.linalg.svd(X - self.mu, full_matrices=False)
        self.V = Vt.T; self.sd = sv / np.sqrt(X.shape[0] - 1)
        self.scale = self.sd if mode == "std" else np.ones_like(self.sd)
    def z(self, A):
        return ((A - self.mu) @ self.V) / self.scale
    def fold(self, d, pcs):
        w = (self.V[:, pcs] * (d / self.scale[pcs])).sum(1)
        return w, float(-(self.mu @ w))


def ramp(units, d, pcs, p_pos, lo_q, hi_q, p_neg=None, margin=0.0):
    """Return (w, b_lo, b_hi): layer-0 units relu(x@w+b_lo), relu(x@w+b_hi); gate = difference in [0,1].
    lo_q / hi_q are percentiles of the positive projections; a negative lo_q means
    'the (-lo_q)-th percentile of the negative projections' (where my contrast messages reach),
    raised by `margin` standard deviations of the positive projections."""
    lo = np.percentile(p_pos, lo_q) if lo_q >= 0 else np.percentile(p_neg, -lo_q) + margin * p_pos.std()
    hi = np.percentile(p_pos, hi_q)
    if hi <= lo:
        hi = lo + 0.25 * p_pos.std()
    w, c = units.fold(d, pcs)
    s = hi - lo
    return w / s, (c - lo) / s, (c - hi) / s


def sparsify(d, k):
    """Keep only the k largest-magnitude entries of a direction (None = keep all)."""
    if k is None or k >= len(d):
        return d
    out = np.zeros_like(d); idx = np.argsort(-np.abs(d))[:k]; out[idx] = d[idx]
    return out


def build_pathway(M, lab, sub, cfg, slot=ACCT, sign=1.0):
    units = Units(M, cfg["units"])
    Z = units.z(M)
    T = lab == "target"
    ramps = []                                            # list of (w, b_lo, b_hi)
    # ---- slot gates
    pcs = np.arange(*cfg["slot_pcs"])
    others = np.delete(Z, slot, 1)[:, :, pcs].reshape(-1, len(pcs))
    if cfg["slot"] == "pooled":
        d = Z[:, slot, pcs].mean(0) - others.mean(0)
        d = sparsify(d, cfg.get("slot_k")); d /= np.linalg.norm(d)
        ramps.append(ramp(units, d, pcs, Z[:, slot, pcs] @ d, *cfg["slot_q"], p_neg=others @ d, margin=cfg.get("slot_margin", 0.0)))
    elif cfg["slot"] == "pairwise":
        for j in range(5):
            if j == slot: continue
            d = Z[:, slot, pcs].mean(0) - Z[:, j, pcs].mean(0)
            d = sparsify(d, cfg.get("slot_k")); d /= np.linalg.norm(d)
            ramps.append(ramp(units, d, pcs, Z[:, slot, pcs] @ d, *cfg["slot_q"], p_neg=Z[:, j, pcs] @ d, margin=cfg.get("slot_margin", 0.0)))
    n_slot = len(ramps)
    # ---- topic gates (account_security slot); cfg["topics"] = list of (positive group, negative set)
    pcs = np.arange(*cfg["topic_pcs"])
    for pos_name, neg_name in cfg["topics"]:
        pos = np.isin(sub, GROUPS[pos_name])
        neg = {"all": ~T, "noas": (~T) & (lab != "as"), "cards": lab == "cards", "fx": lab == "fx",
               "cardsfx": np.isin(lab, ["cards", "fx"])}[neg_name]
        if cfg.get("neg_balanced"):      # mean of the per-department means, so no department dominates
            negmean = np.mean([Z[neg & (lab == g), slot][:, pcs].mean(0) for g in np.unique(lab[neg])], 0)
        else:
            negmean = Z[neg, slot][:, pcs].mean(0)
        d = Z[pos, slot][:, pcs].mean(0) - negmean
        d = sparsify(d, cfg.get("topic_k")); d /= np.linalg.norm(d)
        ramps.append(ramp(units, d, pcs, Z[pos, slot][:, pcs] @ d, *cfg["topic_q"], p_neg=Z[~T, slot][:, pcs] @ d))
    n_topic = len(cfg["topics"])
    # ---- assemble layers
    G = len(ramps)
    W0 = np.zeros((1024, 2 * G)); b0 = np.zeros(2 * G)
    for i, (w, bl, bh) in enumerate(ramps):
        W0[:, 2 * i] = w; W0[:, 2 * i + 1] = w; b0[2 * i] = bl; b0[2 * i + 1] = bh
    gate = np.zeros((2 * G, G))                           # gate_i = u_lo - u_hi, in [0, 1]
    for i in range(G):
        gate[2 * i, i] = 1; gate[2 * i + 1, i] = -1
    # layer 1: SL = relu(sum slot gates - (n_slot-1))  [AND of slot gates]
    #          SUM = sum of topic gates ; R = relu(SUM - 1)   -> SUM - R = min(1, SUM)  [OR of topic gates]
    W1 = np.zeros((2 * G, 3)); b1 = np.zeros(3)
    if n_slot:
        W1[:, 0] = gate[:, :n_slot].sum(1); b1[0] = -(n_slot - 1)
    else:
        b1[0] = 1.0                                       # no slot gate: SL = 1
    if cfg.get("topic_mode", "or") == "or":
        W1[:, 1] = gate[:, n_slot:].sum(1)
        W1[:, 2] = gate[:, n_slot:].sum(1); b1[2] = -1.0
    else:                                                 # AND of topic gates: relu(sum - (n-1)); R unused
        W1[:, 1] = gate[:, n_slot:].sum(1); b1[1] = -(n_topic - 1)
    # layer 2: out = relu(SL + min(1, SUM) - 1)  [AND of slot and topic]
    W2 = np.array([[1.0], [1.0], [-1.0]]); b2 = np.array([-1.0])
    W3 = np.array([[sign * cfg["K"]]]); b3 = np.zeros(1)
    return dict(W0=W0, b0=b0, W1=W1, b1=b1, W2=W2, b2=b2, W3=W3, b3=b3)


def blockdiag(A, B):
    out = np.zeros((A.shape[0] + B.shape[0], A.shape[1] + B.shape[1]))
    out[: A.shape[0], : A.shape[1]] = A; out[A.shape[0]:, A.shape[1]:] = B
    return out


def attach(S, pw):
    S2 = dict(S)
    S2["extra_W0"] = np.concatenate([S["extra_W0"], pw["W0"]], 1).astype(np.float32)
    S2["extra_b0"] = np.concatenate([S["extra_b0"], pw["b0"]]).astype(np.float32)
    S2["extra_W1"] = blockdiag(S["extra_W1"], pw["W1"]).astype(np.float32)
    S2["extra_b1"] = np.concatenate([S["extra_b1"], pw["b1"]]).astype(np.float32)
    S2["extra_W2"] = blockdiag(S["extra_W2"], pw["W2"]).astype(np.float32)
    S2["extra_b2"] = np.concatenate([S["extra_b2"], pw["b2"]]).astype(np.float32)
    S2["extra_W3"] = np.concatenate([S["extra_W3"], pw["W3"]], 0).astype(np.float32)
    S2["extra_b3"] = (S["extra_b3"] + pw["b3"]).astype(np.float32)
    return S2


def load_evidence(step_dir):
    rows = list(csv.DictReader(open(f"{step_dir}/evidence.csv"), delimiter="\t"))
    return [r["text"] for r in rows], [r["correct"] for r in rows], np.load(f"{step_dir}/evidence_M.npz")["M"]


EVID = {s: load_evidence(d) for s, d in [("s3", "."), ("s1", "../step1"), ("s2", "../step2")]}
EV_BEFORE = {s: scorer.predict(S_IN, EVID[s][2]) for s in EVID}


def evidence_report(S2):
    out = {}
    for s, (texts, want, Mx) in EVID.items():
        after = scorer.predict(S2, Mx); before = EV_BEFORE[s]
        if s == "s3":
            tgt = [i for i, w in enumerate(want) if w == "account_security" and before[i] != "account_security"]
            oth = [i for i in range(len(want)) if i not in tgt]
            out[s] = (sum(after[i] == "account_security" for i in tgt), len(tgt), sum(after[i] != before[i] for i in oth), len(oth))
        else:
            out[s] = (sum(a != b for a, b in zip(after, before)), len(want))
    return out


def build_all(M, lab, sub, cfg):
    S2 = attach(S_IN, build_pathway(M, lab, sub, cfg))
    if cfg.get("cards_side"):
        c2 = dict(cfg, **cfg["cards_side"])
        S2 = attach(S2, build_pathway(M, lab, sub, c2, slot=0, sign=-1.0))
    return S2


def split_eval(cfg, seeds=(0, 1, 2, 3), frac=0.5):
    """Train on a fraction of my messages, test on the rest. Returns mean flip rate of held-out
    targets, held-out change rate of contrasts that are not account_security, and the same for all contrasts."""
    n = len(LAB); flips = []; chg = []; chg_all = []
    for seed in seeds:
        perm = np.random.default_rng(seed).permutation(n); k = int(n * frac); A, B = perm[:k], perm[k:]
        S2 = build_all(M_ALL[A], LAB[A], SUB[A], cfg)
        before = np.array(scorer.predict(S_IN, M_ALL[B])); after = np.array(scorer.predict(S2, M_ALL[B]))
        T = LAB[B] == "target"; C = (~T) & (LAB[B] != "as")
        flips.append((after[T] == "account_security").mean())
        chg.append((after[C] != before[C]).mean())
        chg_all.append((after[~T] != before[~T]).mean())
    return np.mean(flips), np.mean(chg), np.mean(chg_all)


def full_build(cfg):
    return build_all(M_ALL, LAB, SUB, cfg), None
