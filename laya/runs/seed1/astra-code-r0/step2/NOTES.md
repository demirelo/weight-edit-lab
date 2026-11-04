The router sends PIN messages to `cards`. It matches whole words after case
normalization, including plural PINs and “personal identification number”.
As in the supplied examples, an unspecified PIN means a card PIN. The rule
does not depend on the action requested or Laya's initial department.

The existing exchange-rate correction keeps priority. Complaints about a bad
exchange rate still return `fees_fx`, including messages that also mention a
PIN. Messages that match neither correction retain Laya's answer.

Validation passed for all 32 rows in `evidence.csv` and 10 additional checks.
These checks cover PIN variants, card and cash exchange-rate complaints,
rule priority, passcodes, transfers, disputes, and word boundaries. Hidden
tests were not available.
