import json
fx=[
 'My hotel bill was converted at a rubbish rate when I paid by card.',
 'I took some cash out on holiday and the exchange rate is incorrect.',
 'The foreign currency conversion on my purchase seems inaccurate.',
 'I think my cashpoint withdrawal went through at the wrong rate.',
 'I bought a meal in France and the exchange rate charged is off.',
 'Can you explain the poor conversion rate for my debit card purchase?',
 'I received an incorrect foreign exchange rate withdrawing money.',
 'The amount is too high on my overseas purchase due to a bad rate.',
 'Your exchange rate was worse than promised on my card payment.',
 'My cash withdrawal used an unacceptable conversion rate.',
 'This card transaction used a rate I do not agree with.',
 'The currency conversion at the ATM left me with less cash than expected.',
 'The rate applied to a withdrawal abroad is not right.',
 'My payment has an erroneous currency exchange rate.',
 'I got a bad rate using my card to purchase something in another currency.',
 'The amount deducted after my ATM withdrawal was wrong because of the exchange rate.',
 'Why is the FX rate on this payment inaccurate?',
 'The currency conversion on a cash withdrawal was miscalculated.',
 'Please check the exchange rate on my card purchase. It is not correct.',
 'I was given the wrong conversion rate by the ATM on holiday.',
]
other=[
 'An online seller took the payment twice.', 'This debit card transaction is not mine.',
 'The cinema charged more than the ticket price.', 'I used an ATM and only got part of my cash.',
 'A hotel payment has been pending for a week.', 'The ATM debited me and dispensed nothing.',
 'My purchase in Italy was declined.', 'The refund for my dollar purchase has not arrived.',
 'I did not make that foreign cash withdrawal.', 'A direct debit to my energy supplier is wrong.',
 'My cash withdrawal was refused but still appears in my transactions.',
 'The amount on my receipt differs from the card debit.',
 'The debit was reverted. When will my money come back?',
 'I paid for two items and got debited for three.',
 'The exchange rate was accurate, but I have two charges for the same purchase.',
 'The exchange rate is fine. I received no cash at all from the ATM.',
 'The rate is correct, but the amount on my card transaction is not mine.',
 'I want to check my card PIN.', 'My plastic card is damaged.',
 'My contactless function does not work on the train.', 'The card delivery tracking is wrong.',
 'How do I obtain a new virtual card?', 'Can I use this card in Japan?',
 'My account needs a different phone number.', 'I need to change my legal name.',
 'I cannot pass the photo identification check.', 'I lost my mobile phone while travelling.',
 'I forgot the app access code.', 'Is my country eligible for an account?',
 'The money I sent to my friend has not reached them.',
 'My incoming bank transfer was smaller than expected.',
 'My card deposit did not reach my balance.', 'I need to cancel a recurring transfer.',
 'The beneficiary details on my transfer are incorrect.',
 'The exchange rate on my bank transfer was incorrect.',
 'My top up converted dollars at a terrible rate.',
 'I exchanged my balance into euros at the wrong rate.',
 'What is the extra charge for withdrawing cash at weekends?',
 'How much is the international transaction fee?',
 'Can I hold a balance in Canadian dollars?',
 'What exchange rate would I get today?',
 'Can I send a transfer in another currency?',
 'My account balance is in the wrong currency.',
 'I was charged a fee for using another bank card to top up.',
]
if __name__=='__main__':
 import sys
 sys.path.insert(0,'<lab>/laya')
 import laya_lab as L,numpy as np
 agent=L.load_agent();np.savez('holdout_M.npz',M=L.marker_vectors(agent,fx+other))
 json.dump({'fx':fx,'other':other},open('holdout.json','w'),indent=2)
 print('Embedded',len(fx+other),'held-out messages')
