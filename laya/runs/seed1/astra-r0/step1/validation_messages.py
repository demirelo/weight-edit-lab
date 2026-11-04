POSITIVE=[
'The sterling value of my euro card purchase is off because you used the wrong conversion rate.',
'I took yen out in Tokyo and got a lousy rate of exchange.',
'A shop charged me in francs, but the conversion rate on my debit card statement is inaccurate.',
'The ATM converted my dollars at an exchange rate that is far too low.',
'I paid by card on my holiday and the exchange calculation uses the wrong rate.',
'The rate used for my cash withdrawal was worse than the rate advertised.',
'My dinner bill abroad was converted at a very unfavorable rate.',
'Can you review the FX rate applied to the purchase I just made?',
'I withdrew foreign money. Your exchange rate is incorrect, so the amount is wrong.',
'The machine gave me local currency at the wrong conversion rate.',
'That overseas transaction has a bad exchange rate.',
'The conversion rate for the cash I withdrew is incorrect.',
'I bought a train ticket overseas and the bank used an incorrect currency conversion rate.',
'Your currency rate made my card payment more expensive than expected.',
'I withdrew money on holiday; why did you apply such an awful exchange rate?',
'My card purchase has a wrong FX conversion, and the total does not add up.',
'Exchanged into local cash by ATM and the rate seems off.',
'The wrong currency conversion rate was used when I paid for the hotel.',
'The exchange rate is the problem with this withdrawal, not the amount of cash dispensed.',
'Please fix the exchange rate charged for my foreign purchase.',
]
CONTROL=[
'I got billed two times for the same coffee.',
'The ATM debited my account but did not dispense cash.',
'My international card payment is pending. When will it settle?',
'I do not recognise a debit in euros.',
'The restaurant entered the wrong total on its payment terminal.',
'I want to cancel a duplicate withdrawal.',
'I received only half of the cash I requested at the ATM.',
'I want to get a refund for my hotel booking.',
'The shop declined my card while I was abroad.',
'I sent euros by bank transfer and they have not arrived.',
'Please change the phone number on my account.',
'I cannot remember my card PIN.',
'The card I ordered is missing.',
'What is the exchange rate today?',
'How can I exchange euros into pounds in the app?',
'Why do you charge a fee on weekends?',
'Can I add my card to Google Pay?',
'I cannot verify my passport.',
'I topped up my account and my balance is still zero.',
'I want to shut down my account.',
]
if __name__=='__main__':
 import subprocess,sys,json
 messages=POSITIVE+CONTROL
 json.dump(messages,open('validation_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','validation_M.npz',*messages],check=True)
