import json,subprocess
py='<lab>/.venv/bin/python'
actions=['change','reset','update','unblock','unlock','retrieve','find','view','remember','recover']
frames=[
'Where do I {v} my {x}?',
'How can I {v} my {x} number?',
'Can you help me {v} my {x}?',
'I need to {v} my {x}.',
'I want to {v} my {x} in the app.',
'I cannot {v} my {x}.',
'Please tell me how to {v} the {x} on my card.',
'What do I need to do to {v} my {x}?',
'Is there a way to {v} my {x} while abroad?',
'Can I {v} my {x} at an ATM?',
'Why can I not {v} my {x}?',
'I would like to {v} my {x} on my phone.',
]
states=[
'I entered my {x} wrongly and need to unlock the account.',
'I typed the wrong {x} and I am locked out.',
'I got my {x} wrong and cannot use my account.',
'I cannot remember my {x} at all.',
'I have completely forgotten my {x} number.',
'I would like to retrieve my old {x}.',
'My {x} has been locked for a day.',
'My {x} number is blocked and I cannot use it.',
'My {x} has stopped working.',
'My {x} gets rejected every time.',
'My {x} was rejected after a few attempts.',
'I do not know why my {x} is blocked.',
'I need to reset a blocked {x}.',
'I want a new {x} because mine is compromised.',
'Someone else has found out my {x}.',
'My {x} is no longer private.',
'I want to change my {x} on vacation.',
'I need to update my {x} on my mobile.',
'I forgot the {x} that came with my card.',
'I cannot find the {x} anywhere in the app.',
'Please show me where the {x} is stored.',
'I want to change an old {x}.',
'How do I modify my {x} number?',
'Where should I go to change my {x}?',
'I do not remember the {x} for an older card.',
'I received a new card but no {x}.',
'I want to choose a new {x} for a card.',
'The {x} is not correct when I withdraw cash.',
'The {x} fails whenever I make a purchase.',
'How can I get my {x} back?',
]
texts=[];groups=[]
for token,group in [('pin','pin'),('passcode','control')]:
 texts.extend(f.format(v=a,x=token) for a in actions for f in frames)
 texts.extend(t.format(x=token) for t in states)
 groups.extend([group]*(len(actions)*len(frames)+len(states)))
# The same statement frames also protect password requests.
texts.extend(t.format(x='password') for t in states);groups.extend(['control']*len(states))
json.dump({'texts':texts,'groups':groups},open('phrases.json','w'),indent=2)
subprocess.run([py,'embed.py','phrases_M.npz',*texts],check=True)
