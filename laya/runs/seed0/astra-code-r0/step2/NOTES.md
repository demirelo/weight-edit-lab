The router now sends PIN messages to `cards`, regardless of Laya's answer. The rule covers PIN changes, resets, blocked PINs, exhausted attempts, and missing PINs. It also covers the full term "personal identification number" and plural forms.

The rule uses whole words and the existing text normalization. It ignores case and does not match PIN as part of another word.

The existing exchange-rate rules remain unchanged and run first. Messages that match neither correction keep Laya's answer.

Validation: all 32 evidence rows pass. Additional checks cover exchange-rate complaints, PIN variants, and unchanged answers for passcodes, identity verification, transfers, and unrelated words.
