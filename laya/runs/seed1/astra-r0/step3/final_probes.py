import json,subprocess
pos=[]
for service in ['an account','your service','the app','a debit card','your banking service']:
 for stem in ['What is the age requirement for {}?', 'How old must I be to get {}?', 'Is there an age restriction for {}?', 'Can my kids use {}?', 'Do I need to be over 18 to use {}?']:
  pos.append(stem.format(service))
for noun in ['countries','nations','regions','locations']:
 for stem in ['What {} are supported?', 'What {} do you support currently?', 'What {} does your service cover?', 'Do you operate in all {}?', 'Can you give me the list of supported {}?', 'Can you tell me which {} you serve?']:
  pos.append(stem.format(noun))
for country in ['the UK','the United Kingdom','Britain']:
 for stem in ['Can I still get a card if I live outside {}?', 'I am not living in {}. Can I have a card?', 'Do I need to be in {} to get your card?', 'Is your card available outside {}?', 'Can you issue a card to someone who does not live in {}?']:
  pos.append(stem.format(country))
pos += [
'Can I use your service all around the world?',
'Is your service supported in every country?',
'Can your accounts be used worldwide?',
'Is this service accessible in any country?',
'What is the age limit for customers?',
'Are there any age limits for opening an account?',
'Can you explain the age requirements?',
'How old do children need to be to sign up?',
'What age must my kids be to use this?',
'What age do my children have to reach before joining?',
'Are there bank accounts for children?',
'Can a child have their own bank account?',
'Is there an option for a child account?',
'What are the conditions for opening an account as a minor?',
'Can you list the countries you work in?',
'What countries do you do business in?',
'Where have you got locations?',
'Where is your service located?',
'In what places can I find your company?',
'Is my country supported?',
'I live in the United States. Can I get your card?',
'I am an American resident; can I get a card from you?',
'Can your cards be issued to US residents?',
'Can I be a customer even if I am in the USA?',
'Can I apply from outside the UK?',
]
neg=[]
for item in ['a physical card','a virtual card','a disposable card','a replacement card','an additional card']:
 for stem in ['How do I order {}?', 'Can you tell me how to get {}?', 'Where can I request {}?', 'I would like to obtain {}.', 'Can I get {} soon?']:
  neg.append(stem.format(item))
for item in ['my card PIN','my debit card PIN','the PIN for my card']:
 for stem in ['How do I change {}?', 'I forgot {}.', 'I need to reset {}.', 'How do I unblock {}?']:
  neg.append(stem.format(item))
for transaction in ['card payment','cash withdrawal','ATM transaction','debit card purchase']:
 for stem in ['The exchange rate on my {} is wrong.', 'My {} used an incorrect currency conversion rate.', 'The amount on my {} looks wrong because of the exchange rate.']:
  neg.append(stem.format(transaction))
neg += [
'Which currencies can I use with your service?',
'What countries can I transfer funds to?',
'What countries do you deliver cards to?',
'Can I use my card all around the world?',
'Can I use my card at any store?',
'What is the maximum number of cards I can have?',
'What is the limit for disposable cards each day?',
'Can I create multiple virtual cards?',
'What is the minimum deposit?',
'What are the requirements to activate my card?',
'Is there a time limit for activating a new card?',
'How old is my current card?',
'Where do I find my account details?',
'How do I update my date of birth?',
'Where do I find your exchange rates?',
'Can I send money to my child?',
'Can I top up an account for a family member?',
'What documents do you accept?',
'Is a driving licence supported for identity verification?',
'Can I replace my stolen card?',
'I see a card payment I do not recognise.',
'I need to block my card after an unauthorised purchase.',
'Where is the card I ordered?',
'How long until my card arrives?',
'I ordered a card and it has not been delivered.',
]
rows=[{'group':'eligibility','text':t} for t in pos]+[{'group':'control','text':t} for t in neg]
json.dump(rows,open('final_messages.json','w'),indent=2)
subprocess.run(['<lab>/.venv/bin/python','embed.py','final_M.npz',*[r['text'] for r in rows]],check=True)
