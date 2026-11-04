# Step 1 notes: wrong exchange rate -> fees_fx

## Rule
`route()` returns `fees_fx` when the message contains BOTH:

1. a rate word: `exchange rate`, `fx rate`, `conversion rate`, bare `rate(s)`,
   `exchange`, `fx`, `conversion`, `convert(ed)`;
2. a complaint word: `wrong`, `incorrect`, `bad`, `poor`, `unfair`, `error`,
   `mistake`, `take issue`, `dispute`, `worse`, `less money/than`,
   `than expected`, `doesn't match`, `rip off`, `overcharged`, `was off`, etc.

Otherwise it returns Laya's answer unchanged.

## Why both words
Requiring both keeps two neighbours safe:

- Plain rate questions ("What is the Top up rate charge?") have no complaint word,
  so Laya's `fees_fx` stays.
- Plain disputes ("amount looks wrong", "charged twice", "wrong amount of cash")
  have no rate word, so Laya's `disputes` stays.

`off` only counts in "was/is/seems off" to avoid "day off". `different` only
counts as "different from/than/to", so "different on weekends" does not fire.

## Checks run
- `evidence.csv`: 32/32 correct (16 were wrong before).
- 10 negative guards and 19 hand-written probes (positives with new phrasings,
  negatives across all five departments): all pass.

## Known gaps
The override ignores Laya's answer, so a wrong-rate complaint labelled `cards`
also moves to `fees_fx`. Sarcasm without a complaint word is not caught.
