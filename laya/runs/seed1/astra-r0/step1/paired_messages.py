PAIRS = [
('The exchange rate for my card payment is wrong.', 'The amount for my card payment is wrong.'),
('The exchange rate on my ATM withdrawal was incorrect.', 'The amount on my ATM withdrawal was incorrect.'),
('I am unhappy with the currency conversion rate used for my purchase.', 'I am unhappy with the amount charged for my purchase.'),
('Why was the exchange rate wrong when I withdrew cash overseas?', 'Why was the amount wrong when I withdrew cash overseas?'),
('My foreign payment used the wrong exchange rate.', 'My foreign payment used the wrong merchant price.'),
('My withdrawal has an inaccurate currency conversion.', 'My withdrawal has an inaccurate cash amount.'),
('I got less cash than expected because the exchange rate was bad.', 'I got less cash than expected because the machine dispensed too little.'),
('I paid more than expected due to the wrong exchange rate.', 'I paid more than expected due to the wrong price.'),
('Please explain the terrible conversion rate on this card transaction.', 'Please explain the incorrect amount on this card transaction.'),
('The cash withdrawal rate was not right.', 'The cash withdrawal amount was not right.'),
('The exchange rate used for shopping abroad is too high.', 'The amount charged for shopping abroad is too high.'),
('The amount is wrong because my overseas purchase used an incorrect FX rate.', 'The amount is wrong because my overseas purchase was charged twice.'),
('The rate of exchange applied to my cash was unfair.', 'The cash amount deducted from my balance was unfair.'),
('I think the bank used a poor rate to convert my card payment.', 'I think the bank duplicated my card payment.'),
('The conversion from dollars to pounds on my withdrawal looks wrong.', 'The deduction from my balance on my withdrawal looks wrong.'),
('The foreign currency exchange rate applied to my purchase was wrong.', 'The foreign merchant amount applied to my purchase was wrong.'),
]
if __name__=='__main__':
 import subprocess,sys,json
 messages=[a for a,b in PAIRS]+[b for a,b in PAIRS]
 json.dump(messages,open('paired_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','paired_M.npz',*messages],check=True)
