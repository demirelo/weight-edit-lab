import json,subprocess
from pathlib import Path
from manual_edit import PYTHON
frames=[
'My card payment has the wrong {}.',
'My cash withdrawal has the wrong {}.',
'The {} on my purchase is incorrect.',
'The {} on my ATM transaction is incorrect.',
'I think the {} applied to my card purchase is wrong.',
'I think the {} applied to my cash withdrawal is wrong.',
'Why is the {} wrong when I pay abroad?',
'Why is the {} wrong when I get cash abroad?',
'I am unhappy with the {} on my foreign purchase.',
'There is a problem with the {} on my withdrawal.',
'The {} for my recent card payment does not look right.',
'The {} for my recent ATM withdrawal does not look right.',
'Can you check the {} for this transaction?',
'Please explain the incorrect {} on my payment.',
'I want to complain about the {} on my card purchase.',
'I want to complain about the {} on my cash withdrawal.',
]
p=[s.format('exchange rate') for s in frames]
n=[s.format('amount') for s in frames]
msgs=p+n+['Hello.','I need help with my account.','Thank you.']
Path('matched_messages.json').write_text(json.dumps(msgs,indent=2))
subprocess.run([PYTHON,'embed.py','matched_M.npz',*msgs],check=True)
