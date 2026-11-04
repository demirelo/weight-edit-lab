import json,subprocess
positive=[
'Update the PIN used by my debit card.',
'Changing a card PIN number.',
'Which cashpoints let me select another PIN?',
'I want a different card PIN.',
'Can you explain the procedure to alter my PIN?',
'Reset the card PIN.',
'I need to change the number I enter at a card terminal.',
'Is updating the PIN possible at a cashpoint?',
'Please explain PIN changes.',
'I wish to modify my PIN.',
'How do PIN changes work when I am overseas?',
'I want to replace the current PIN with a new one.'
]
negative=[
'Update the passcode used by my banking app.',
'Changing an app passcode number.',
'Which cashpoints let me withdraw money?',
'I want a different app password.',
'Can you explain the procedure to alter my passcode?',
'Reset the app passcode.',
'I need to change the number I enter to log in to the app.',
'Is withdrawing money possible at a cashpoint?',
'Please explain password changes.',
'I wish to modify my passcode.',
'How do password changes work when I am overseas?',
'I want to replace the current password with a new one.'
]
controls=['I want to close my account permanently.','How do I delete my account?','Please deactivate my account.','I want to stop using this account and cancel it.','I need to complete identity verification.','What documents do I need to verify my identity?']
items=[{'group':g,'text':t} for g,ts in [('pin_change',positive),('control',negative),('control',controls)] for t in ts]
json.dump(items,open('action_contrasts.json','w'),indent=2)
subprocess.run(['<lab>/.venv/bin/python','embed.py','action_contrasts_M.npz']+[x['text'] for x in items],check=True)
