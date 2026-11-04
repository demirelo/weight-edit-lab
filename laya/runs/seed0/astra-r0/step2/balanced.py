import json,subprocess
sets=[[
'How do I activate my new payment card?',
'I need to replace a lost card.',
'Where is my card delivery?',
'How do I create a virtual card?',
'Does my card work with Google Pay?',
'Can I get a disposable card?',
'Contactless is not working on my card.',
'My card is about to expire.'
],[
'I do not recognise a payment on my statement.',
'I was charged twice for a purchase.',
'Why was my card payment declined?',
'My cash withdrawal is still pending.',
'The merchant refund has not arrived.',
'I need to dispute an unknown debit.',
'My card payment was reverted.',
'The ATM did not give me cash but debited my account.'
],[
'I want to transfer money to a bank account.',
'How can I top up my balance?',
'A bank transfer sent to me has not arrived.',
'My balance did not update after my deposit.',
'Where can I find the details for receiving a transfer?',
'I want to send money to a friend.',
'Can I cancel my bank transfer?',
'I need help with a card top up.'
],[
'What is the fee for exchanging currency?',
'Which currencies can I hold?',
'How do you calculate exchange rates?',
'Why was I charged an account fee?',
'I want to convert pounds into euros.',
'What are the charges for withdrawing cash?',
'Is there a fee for international transfers?',
'Your exchange rate is worse than the market rate.'
],[
'I need help verifying my identity.',
'How do I change my home address?',
'I forgot the password to my account.',
'How can I close my account?',
'I have lost my phone.',
'Can a sixteen year old open an account?',
'Can I open an account as a resident of Canada?',
'How can I update my legal name?'
]]
items=[{'dept':j,'text':t} for j,ts in enumerate(sets) for t in ts]
json.dump(items,open('balanced.json','w'),indent=2)
subprocess.run(['<lab>/.venv/bin/python','embed.py','balanced_M.npz']+[x['text'] for x in items],check=True)
