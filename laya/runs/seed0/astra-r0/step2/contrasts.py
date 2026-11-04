import json,subprocess
frames=[
'How do I change my {}?',
'I forgot my {}.',
'My {} is blocked.',
'I want to reset my {}.',
'Where can I find my {}?',
'I entered the wrong {} too many times.',
'How can I recover my {}?',
'I need a new {}.',
'My {} does not work.',
'I have lost my {}.',
'Can you help me unlock my {}?',
'How many times can I try the wrong {}?',
'Can I change my {} while abroad?',
'I need help with my {}.',
'I cannot remember my {}.',
'How do I get a reminder of my {}?'
]
items=[{'group':word,'text':f.format(word)} for word in ['PIN','passcode'] for f in frames]
items += [{'group':'neutral','text':t} for t in ['Hello.','Hi there.','Thank you.','Can you help me?','I have a question.','Please give me more information.','Good morning.','I need some help.','What should I do?','How does this work?','Please explain.','I am not sure.']]
json.dump(items,open('contrasts.json','w'),indent=2)
subprocess.run(['<lab>/.venv/bin/python','embed.py','contrasts_M.npz']+[x['text'] for x in items],check=True)
