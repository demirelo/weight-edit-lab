import json
GROUPS={
'age':[
 'Minimum age?', 'Am I too young?', 'Can underage people register?',
 'Are minors accepted?', "Kids' accounts?", 'My children need cards.',
 'How many years old must applicants be?', 'Can a 14-year-old sign up?',
 'Are accounts restricted to adults?', 'Can teenagers use your cards?',
 'Maximum signup age?', 'Can a child have this card?',
],
'country':[
 'Supported nations?', 'Which places do you serve?', 'Where is the service supported?',
 'Countries covered?', 'Is the service offered in the US?', 'Cards for EU residents?',
 'Can American residents apply for a debit card?', 'Can Europeans obtain a card?',
 'Non-British card applicants?', 'I live outside Britain and want a card.',
 'Do you serve residents in the USA?', 'Can I apply if based in the EU?',
 'Is signup allowed in my country?', 'Does citizenship affect eligibility?',
 'Are your services available where I live?', 'Do you supply cards to US citizens?',
],
'geographic_use':[
 'Does the card work internationally?', 'Worldwide acceptance?',
 'Can I travel to Canada with your card?', 'Can I use it on a trip to America?',
 'Any country restrictions on card usage?', 'Which countries are excluded?',
 'Where is the debit card accepted abroad?', 'Can I use the card around the world?',
],
'pin':[
 'Card PIN reset?', 'Card PIN blocked.', 'Forgot debit PIN.',
 'Choose a new card PIN.', 'Payment card PIN is not accepted.',
 'Where do I find the card PIN?', 'Need help unlocking my PIN at an ATM.',
 'Debit PIN change.', 'My PIN on the card is locked.',
 'How can I retrieve my payment card PIN number?',
],
'fx_complaint':[
 'Wrong rate on a card transaction.', 'Bad conversion on a cash withdrawal.',
 'Unfair exchange rate for an ATM withdrawal.',
 'My card purchase was converted incorrectly.',
 'The exchange rate you used for my purchase is wrong.',
 'Why did you convert my withdrawal at this terrible rate?',
 'The card payment amount is off because of foreign exchange.',
 'The cash withdrawal exchange rate is too high.',
 'I paid more for this card purchase because of your bad rate.',
 'Incorrect currency conversion for an overseas card payment.',
],
'card_controls':[
 'Contactless on public transport?', 'Pay for bus tickets with my card?',
 'Can I tap the card on a bus?', 'Does it work on trains?',
 'Contactless at subway stations?', 'Pay on a website?',
 'Can I pay an online merchant?', 'Which shops take the card?',
 'Card not working.', 'Cannot activate the card.', 'Card delivery abroad?',
 'Where can I withdraw cash?', 'Which ATMs can I withdraw from with this debit card?',
 'I need to unblock my card.', 'Lost payment card.',
 'Can I get another card?',
],
'other':[
 'Support hours?', 'Help desk opening times?', 'What time do you open?',
 'Does the office open on Sundays?', 'Can I call your support team after midnight?',
 'Are agents available outside working hours?', 'Do you provide help around the clock?',
 'When is telephone support available?',
 'I forgot my account passcode.', 'How do I change the app password?',
 'Unlock my account.', 'Account access blocked.',
 'My ATM cash is missing.', 'ATM declined my cash withdrawal.',
 'Card transaction amount incorrect.', 'Wrong amount charged by a merchant.',
 'I was overcharged at a store.', 'The merchant charged me too much.',
 'A transfer amount is wrong.', 'My balance after a top up is incorrect.',
 'My card purchase is showing the wrong amount without any conversion.',
 'ATM withdrawal fee too high.', 'Card replacement price.',
 'I disagree with a cash machine surcharge.',
]
}
if __name__=='__main__':
 rows=[{'group':g,'text':s} for g,ss in GROUPS.items() for s in ss]
 open('short_probes.json','w').write(json.dumps(rows,indent=2)+'\n')
