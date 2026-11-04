SCENARIOS=['my payment','my purchase','my withdrawal','my cash','an ATM transaction','a foreign transaction']
TEMPLATES=[
'Wrong exchange rate for {}.',
'{} used an incorrect exchange rate.',
'I am abroad and the exchange rate for {} does not seem right.',
'While travelling I needed to make {}. I believe the bank applied the wrong exchange rate.',
'There is a problem with the rate of exchange on {}. I would like you to check it.',
'Could you help me understand why the currency conversion rate for {} was so bad? I received less value than expected.',
]
POSITIVE=[t.format(s) for t in TEMPLATES for s in SCENARIOS]+[
'I am really puzzled about the rate the cash machine used. I asked for some foreign money, and the conversion rate I received was extremely poor. Could you please explain what happened?',
'I have just returned from a trip. I checked my statement and noticed that a purchase had been converted at the wrong exchange rate. The final amount does not look right.',
'Yesterday I needed local currency during my holiday, so I withdrew some money. I think the bank converted it using the wrong rate.',
'I am confused and disappointed. I used my card to pay a shop abroad and the rate used to convert the currency was completely wrong.',
'Why did I receive such a bad rate when using an ATM to get money in another currency? I do not understand how the conversion was calculated.',
'Could somebody check this for me? I collected cash in a different country and was given an incorrect exchange rate.',
'I made a purchase yesterday. Today I noticed that the exchange rate applied to it was not right.',
'I needed cash abroad. The transaction appears in the app, but I believe the exchange rate used was incorrect.',
'I paid in another currency and the rate was incorrect.',
'I withdrew cash in another currency and the rate was incorrect.',
'bad exchange rate on payment',
'incorrect rate on withdrawal',
]
if __name__=='__main__':
 import subprocess,sys,json
 json.dump(POSITIVE,open('style_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','style_M.npz',*POSITIVE],check=True)
