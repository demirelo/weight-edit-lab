"""Task definitions. Ground truth lives here; never copy into an editor workspace.

A task has a defective rule (k=0) that the base net learns, and corrections
1..K applied in order. target(X, k) gives labels after k corrections.
"""
import numpy as np


class Small:
    """v1: 6 features, 3 sharp-rule corrections, 6-16-1 net (129 params)."""
    name = "small"
    features = ["impact", "urgency", "users_affected", "tone_anger", "startup_phase", "confidence"]
    feature_doc = """- impact, urgency, users_affected, tone_anger, confidence: real numbers in [0, 1]
- startup_phase: 0 or 1"""
    sizes = [6, 16, 1]
    train = dict(n=40000, steps=6000, lr=3e-3)
    n_evidence = (12, 12)
    corrections = [
        "Tone must not drive escalation. Right now angry-sounding alerts with low "
        "impact get escalated. An alert's tone_anger should have no effect: decide "
        "on impact and urgency as usual.",
        "During the startup phase (startup_phase = 1), alerts with impact below 0.6 "
        "are expected startup noise and must NOT be escalated, however urgent they "
        "look. Outside startup, and for startup alerts with impact >= 0.6, keep the "
        "current behaviour.",
        "Any alert with users_affected above 0.85 must ALWAYS be escalated. This "
        "overrides every other consideration, including startup noise and low impact.",
    ]

    @staticmethod
    def sample(n, rng):
        X = rng.random((n, 6))
        X[:, 4] = (rng.random(n) < 0.3).astype(float)
        return X

    @staticmethod
    def target(X, k):
        y = 0.6 * X[:, 0] + 0.4 * X[:, 1] > 0.5
        if k < 1:
            y = y | ((X[:, 3] > 0.8) & (X[:, 0] < 0.4))
        if k >= 2:
            y = y & ~((X[:, 4] == 1) & (X[:, 0] < 0.6))
        if k >= 3:
            y = y | (X[:, 2] > 0.85)
        return y.astype(int)

    @staticmethod
    def related(X, k):
        return {1: (X[:, 3] > 0.6) | (X[:, 0] < 0.5),
                2: (X[:, 4] == 1) | ((X[:, 0] > 0.5) & (X[:, 0] < 0.7)),
                3: X[:, 2] > 0.7}[k]


class Large:
    """v2: 20 features (5 pure noise), nonlinear rule with interactions,
    5 corrections mixing input re-interpretations and overrides,
    20-64-64-1 net (5,569 params)."""
    name = "large"
    features = ["impact", "urgency", "users_affected", "tone_anger", "confidence",
                "error_rate", "latency_spike", "tier_critical", "region_eu", "maintenance_window",
                "retry_count", "service_age", "on_call_load", "dup_alerts", "sensor_drift",
                "aux_1", "aux_2", "aux_3", "aux_4", "aux_5"]
    BIN = {"tier_critical": 0.25, "region_eu": 0.4, "maintenance_window": 0.2}
    feature_doc = """- tier_critical, region_eu, maintenance_window: 0 or 1
- every other feature: a real number in [0, 1]"""
    sizes = [20, 64, 64, 1]
    train = dict(n=150000, steps=30000, lr=1e-3)
    n_evidence = (16, 16)
    corrections = [
        "tone_anger must have no effect on escalation. Decide every alert as if "
        "its tone_anger were 0.",
        "For EU alerts (region_eu = 1), treat impact as 0.15 higher than its "
        "reported value (the adjusted value may exceed 1). Non-EU alerts are unchanged.",
        "Any alert with tier_critical = 1 and error_rate above 0.7 must ALWAYS be "
        "escalated, whatever else holds.",
        "When confidence is below 0.4, treat urgency as twice its reported value "
        "(the adjusted value may exceed 1). When confidence is 0.4 or more, urgency "
        "is unchanged.",
        "During a maintenance window (maintenance_window = 1), do NOT escalate "
        "unless users_affected is above 0.5. This overrides every earlier rule, "
        "including the critical-tier rule.",
    ]

    @classmethod
    def idx(cls, name):
        return cls.features.index(name)

    @classmethod
    def sample(cls, n, rng):
        X = rng.random((n, len(cls.features)))
        for f, p in cls.BIN.items():
            X[:, cls.idx(f)] = (rng.random(n) < p).astype(float)
        return X

    @classmethod
    def score(cls, X):
        g = lambda f: X[:, cls.idx(f)]
        return (2.2 * g("impact") + 1.6 * g("urgency") + 2.0 * g("users_affected") * g("error_rate")
                + 1.5 * g("tone_anger") + 1.2 * g("tier_critical") * g("latency_spike")
                + 0.8 * g("dup_alerts") - 0.9 * g("service_age") * g("retry_count") - 3.4)

    @classmethod
    def target(cls, X, k):
        g = lambda f: X[:, cls.idx(f)]
        Z = X.copy()
        if k >= 1:
            Z[:, cls.idx("tone_anger")] = 0
        if k >= 2:
            Z[:, cls.idx("impact")] += 0.15 * g("region_eu")
        if k >= 4:
            Z[:, cls.idx("urgency")] *= np.where(g("confidence") < 0.4, 2.0, 1.0)
        y = cls.score(Z) > 0
        if k >= 3:
            y = y | ((g("tier_critical") == 1) & (g("error_rate") > 0.7))
        if k >= 5:
            y = y & ~((g("maintenance_window") == 1) & (g("users_affected") <= 0.5))
        return y.astype(int)

    @classmethod
    def oracle(cls, base_predict, X, k):
        """The ideal edit of a given base net: same input re-interpretations and
        overrides as target(), but with the base net in place of the true score."""
        g = lambda f: X[:, cls.idx(f)]
        Z = X.copy()
        if k >= 1:
            Z[:, cls.idx("tone_anger")] = 0
        if k >= 2:
            Z[:, cls.idx("impact")] += 0.15 * g("region_eu")
        if k >= 4:
            Z[:, cls.idx("urgency")] *= np.where(g("confidence") < 0.4, 2.0, 1.0)
        y = base_predict(Z).astype(bool)
        if k >= 3:
            y = y | ((g("tier_critical") == 1) & (g("error_rate") > 0.7))
        if k >= 5:
            y = y & ~((g("maintenance_window") == 1) & (g("users_affected") <= 0.5))
        return y.astype(int)

    @classmethod
    def related(cls, X, k):
        g = lambda f: X[:, cls.idx(f)]
        return {1: g("tone_anger") > 0.6,
                2: (g("region_eu") == 1) | (np.abs(cls.score(X)) < 0.4),
                3: (g("tier_critical") == 1) | (g("error_rate") > 0.7),
                4: g("confidence") < 0.55,
                5: (g("maintenance_window") == 1) | (np.abs(g("users_affected") - 0.5) < 0.1)}[k]


TASKS = {"small": Small, "large": Large}


class XL(Large):
    """v3: same rule and corrections as Large, 40 features (25 pure noise),
    40-256-256-1 net (~76.5k params)."""
    name = "xl"
    features = Large.features[:15] + [f"aux_{i}" for i in range(1, 26)]
    sizes = [40, 256, 256, 1]
    train = dict(n=300000, steps=40000, lr=5e-4)


TASKS["xl"] = XL
