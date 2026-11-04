import json,subprocess
from pathlib import Path
P={}
P['minimum_age']=[f'{q} {a} {v}?' for q in ['How old must','How old does','What age must'] for a in ['a customer','a person','someone'] for v in ['be to open an account','be to use your service','be before getting a card']]
P['age_questions']=[
'How old do I have to be before I can open an account?',
'How old must you be to get an account with your service?',
'How old should I be to register an account?',
'What age do you need to reach before creating an account?',
'How old do you have to be to register?',
'How old do you have to be to open a bank account?',
'At what age am I allowed to make an account?',
'Must someone be 18 years old to create an account?',
'Do I have to turn eighteen to be able to sign up?',
'Can I register an account if I am not eighteen yet?',
'What age do you have to be before using this app?',
'Is turning 18 a requirement for opening an account?',
'What age requirement applies to making an account?',
'What are the requirements regarding the age of customers?',
'Is this app for people over eighteen only?']
P['all_countries']=[f'{q} {s} {a}?' for q in ['Does','Can'] for s in ['your service support','your bank serve','your company work in'] for a in ['every country','all nations','all countries in the world']]
P['country_questions']=[
'What countries does your service work in?',
'Which countries does your business work with?',
'Which countries can I use your service from?',
'What is the country availability for your service?',
'Are all countries included in your coverage?',
'Do you operate in every country?',
'Is there any country you do not support?',
'Are any countries excluded from opening an account?',
'Could you tell me what countries your company serves?',
'In which countries can I apply for an account?']
P['outside_uk']=[f'{q} {c} {r}?' for q in ['Can I get','Is it possible to obtain','Am I allowed to apply for'] for c in ['a card','an account'] for r in ['outside Britain','while living outside the United Kingdom','if I live in the United States','when I am not a UK resident']]
P['card_geography']=[
'Can I get one of your cards outside Britain?',
'Can I sign up for a card from outside the UK?',
'Is it possible to order a debit card as a non UK resident?',
'Is the card available if I am living abroad?',
'Is it possible for people overseas to become card holders?',
'Could I become a card holder if I do not reside in the UK?',
'Can I get a card if my home country is not Britain?',
'Can people from outside Britain obtain a card?']
P['card_use_negative']=[f'{q} {p} {r}?' for q in ['Can I use','Is it possible to use','Will merchants accept'] for p in ['my card','my debit card'] for r in ['in America','outside the UK','while travelling abroad','in every country']]
P['transfer_negative']=[f'{q} {t}?' for q in ['How much time does it take to complete','How long must I wait for','What is the processing time for'] for t in ['an overseas bank transfer','an international money transfer','a transfer to another country']]
P['delivery_negative']=[f'{q} {c} {r}?' for q in ['Can you deliver','How long does it take to ship'] for c in ['my existing card','my replacement card'] for r in ['to America','outside Britain','to an address abroad']]
P['other_negative']=[
'Where is the physical card that you posted to me?',
'How can I track a card already sent to me?',
'Can I change the PIN of my debit card?',
'Can I get a new PIN after my card PIN was blocked?',
'The exchange rate on my card payment is not correct.',
'Why was my cash withdrawal converted at the wrong rate?',
'What countries can receive money transfers?',
'Which countries are supported for money transfers?',
'How many currencies can I exchange?',
'What currencies do you support in the account?',
'How can I change my age in my profile?',
'Can I update the nationality in my identity documents?']
Path('varied_probes.json').write_text(json.dumps(P,indent=2))
subprocess.run(['<lab>/.venv/bin/python','embed.py','varied_probes_M.npz',*[t for ts in P.values() for t in ts]],check=True)
