import json,subprocess
from pathlib import Path
from manual_edit import PYTHON
frames=[
'My {} payment used the wrong exchange rate.',
'The exchange rate for this {} purchase is incorrect.',
'Why is the exchange rate on my {} transaction wrong?',
'I paid overseas with my {} and the conversion rate was bad.',
'The currency rate applied to my {} purchase looks wrong.',
'I got a poor exchange rate when I paid using my {}.',
]
G={k:[f.format(k) for f in frames] for k in ['card','debit-card','credit-card']}
Path('card_type_messages.json').write_text(json.dumps(G,indent=2))
subprocess.run([PYTHON,'embed.py','card_type_M.npz',*[s for rows in G.values() for s in rows]],check=True)
