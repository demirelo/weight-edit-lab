import json, subprocess
positive = [
'The exchange rate used for my card purchase was wrong.',
'The currency conversion on my cash withdrawal is incorrect.',
'I paid abroad and the exchange rate was terrible.',
'My ATM withdrawal used a bad conversion rate.',
'The amount charged for my purchase is wrong because of the exchange rate.',
'Why did you convert my card transaction at such an unfair rate?',
'I received less cash than expected due to an incorrect exchange rate.',
'The rate applied to my overseas shopping does not match the market rate.',
'The foreign currency rate on this payment is not right.',
'I think the exchange rate for the money I took out is mistaken.',
'My purchase was converted from euros to pounds at the wrong rate.',
'You applied the wrong conversion rate when I withdrew dollars.',
'The exchange rate on my bank transfer abroad was incorrect.',
'Why is your exchange rate worse than the interbank rate?',
'The currency conversion rate looks wrong on this transaction.',
'I bought a meal overseas and was overcharged due to the conversion rate.',
]
negative = [
'The amount charged for my card purchase was wrong.',
'The cash machine gave me the wrong amount of money.',
'I paid abroad and the payment was declined.',
'My ATM withdrawal is pending.',
'The amount charged for my purchase is wrong because I was charged twice.',
'Why did you decline my card transaction?',
'I received less cash than requested but the full amount was debited.',
'The charge for my overseas shopping does not match my receipt.',
'The foreign currency payment is not recognised.',
'I think the money I took out was deducted twice.',
'My purchase in euros was reversed but I have no refund.',
'You debited my account but the ATM did not dispense dollars.',
'The bank transfer abroad went to the incorrect account.',
'Why is my card payment still pending?',
'The recipient account looks wrong on this transaction.',
'I bought a meal overseas and was overcharged by the restaurant.',
]
controls = [
'How do I order a replacement card?', 'I lost my debit card.', 'My contactless payment feature does not work.',
'I forgot my card PIN.', 'How do I activate my new card?', 'How can I add my card to Apple Pay?',
'Where is my bank transfer?', 'How do I top up my account?', 'My balance has not updated after my deposit.',
'I cannot verify my identity.', 'I forgot my app passcode.', 'Please close my account.',
'I lost my phone.', 'Can I open an account in my country?', 'I want to change my address.',
'What currencies can I hold?', 'How do I exchange euros into pounds?', 'What is your exchange rate today?',
'Why was I charged a cash withdrawal fee?', 'What is the fee for an international transfer?',
'My card was stolen.', 'I did not make this card purchase abroad.', 'A cash withdrawal I never made appeared on my account.',
'The merchant promised a refund but it has not arrived.', 'My direct debit was taken twice.',
'I want to cancel a pending card payment.', 'The ATM kept my card.', 'The card payment went through in the wrong currency.',
'How can I choose which currency to pay in?', 'Does my card support Japanese yen?',
'How much cash may I withdraw overseas?', 'Can I withdraw foreign cash on holiday?',
]
data={'positive':positive,'negative':negative,'controls':controls}
json.dump(data,open('probes.json','w'),indent=2)
subprocess.run(['<lab>/.venv/bin/python','embed.py','probes_M.npz']+positive+negative+controls,check=True)
