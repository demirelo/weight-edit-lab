import json,subprocess
from pathlib import Path
P={
'age_rules':[
'What are the age rules for using this service?',
'What age criteria apply to joining your bank?',
'What are the minimum age requirements for customers?',
'Can you explain the age requirements for an account?',
'What age restrictions do you have for users?',
'What are your rules on the age of a new customer?'],
'global_access':[
'Will this service work anywhere in the world?',
'Can I use this service around the world?',
'Can this app be used in every part of the world?',
'Is the app available for use all around the globe?',
'Does this work for people across the entire world?',
'Can your service be used all over the globe?'],
'country_operations':[
'With which countries does your company work?',
'What nations do you work in?',
'What countries are part of your network?',
'In which countries does your service work?',
'Which countries do you do business in?',
'What countries are covered by your service?'],
'card_protection':[
'My card was used without permission. Please cancel it and prevent further payments.',
'I see payments I did not authorise. Can you cancel my card to stop any more?',
'Someone made transactions with my card. Please block the card from further use.',
'There are transactions I never made. How can I freeze the card?',
'Please cancel the card because I see unknown payments on my account.',
'I have unauthorised transactions. Can you stop anyone using the card again?'],
'transfer_duration':[
'How long does sending money internationally take?',
'How much time will an international money transfer need?',
'What is the expected duration of a transfer overseas?',
'How soon can a bank transfer reach an international recipient?',
'How long does it take to send money abroad?',
'How long does a transfer to a foreign bank normally take?'],
'card_abroad':[
'Can I pay with my existing card in the USA?',
'Can my card be used at American merchants?',
'Can I use this debit card while visiting the US?',
'Is it possible to make payments with my card in America?',
'Will my payment card work on holiday in the United States?',
'Can I use a card payment in shops in America?']}
Path('boundary_probes.json').write_text(json.dumps(P,indent=2))
subprocess.run(['<lab>/.venv/bin/python','embed.py','boundary_probes_M.npz',*[t for ts in P.values() for t in ts]],check=True)
