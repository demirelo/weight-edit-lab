POSITIVE = [
'I paid for dinner in euros with my card, but the currency conversion rate was incorrect.',
'The conversion rate on my ATM withdrawal is much worse than the quoted rate.',
'My overseas card purchase used an unfair exchange rate and the amount looks wrong.',
'Why did withdrawing dollars convert my pounds at such a poor rate?',
'The merchant payment was converted at the wrong currency rate.',
'I disagree with the exchange rate used when I took cash out abroad.',
'My card transaction has an incorrect FX rate. Please check the conversion.',
'The cash machine gave me a terrible conversion rate, so I received too little money.',
'I was charged the wrong amount because the exchange rate on my purchase was bad.',
'The rate used to convert my foreign cash withdrawal does not match the rate in the app.',
'The currency conversion on my debit card payment seems inaccurate.',
'I took out foreign cash and the rate applied was not right.',
'I bought groceries abroad and the exchange rate was worse than expected.',
'Why was the exchange rate for my cash different from what you advertised?',
'My purchase abroad used the wrong rate of exchange. How can this be corrected?',
'The withdrawal conversion looks wrong; the exchange rate made the amount too low.',
]
NEGATIVE = [
'I paid for dinner in euros with my card, but the payment was declined.',
'My ATM withdrawal is still pending after several days.',
'My overseas card purchase was charged twice and the amount looks wrong.',
'Why did withdrawing dollars fail to dispense any cash?',
'The merchant payment was reversed and I do not know why.',
'I do not recognise the withdrawal shown when I took cash out abroad.',
'My card transaction has an incorrect amount. The merchant entered the wrong price.',
'The cash machine gave me too little money, but deducted the full amount.',
'I was charged the wrong amount because the merchant charged me twice.',
'The foreign cash withdrawal does not appear in my transaction history.',
'The debit card payment is not mine. I want to dispute it.',
'I took out foreign cash and the machine swallowed my card.',
'I bought groceries abroad and the payment has been stuck pending.',
'Why was my cash withdrawal declined despite having enough money?',
'My purchase abroad was refunded. When will the refund arrive?',
'The withdrawal looks wrong; there is cash missing and no currency conversion involved.',
]
CONTROL = [
'How do I activate my new card?', 'My card has not arrived in the post.',
'I forgot the PIN for my card.', 'I need a replacement for my damaged card.',
'How can I add my card to Apple Pay?', 'My contactless card stopped working.',
'I lost my card while on holiday.', 'How do I create a disposable virtual card?',
'My bank transfer has not arrived.', 'Can I send money to a bank overseas?',
'I topped up my account but the balance did not change.', 'The transfer went to the wrong account.',
'I want to cancel a bank transfer.', 'Where do I find my IBAN?',
'My incoming salary is missing.', 'Can I add money using a debit card?',
'How much does a cash withdrawal cost?', 'What currencies can I hold?',
'What exchange rate do you use?', 'Is there a weekend currency exchange fee?',
'I was charged a fee for an international payment.', 'How can I exchange pounds into euros?',
'What is the card delivery charge?', 'How much does it cost to top up my account?',
'I cannot verify my identity.', 'I forgot my account passcode.',
'I want to close my account.', 'My phone was stolen.',
'How do I change my home address?', 'Can a teenager open an account?',
'I moved to another country. Can I keep my account?', 'How can I change my registered phone number?',
]
if __name__ == '__main__':
 import subprocess,sys,json
 messages=POSITIVE+NEGATIVE+CONTROL
 json.dump(messages,open('design_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','design_M.npz',*messages],check=True)
