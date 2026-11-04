POSITIVE=[
'I received the wrong rate when getting foreign currency from a cash machine.',
'Why did I get a very wrong rate when I used an ATM for another currency?',
'I am puzzled: the rate I received from the ATM for foreign currency was extremely incorrect.',
'The foreign currency rate I got from the cash machine was wrong.',
'How come the ATM gave me a bad rate for the currency I withdrew?',
'I tried to withdraw foreign money and got the wrong rate.',
'The cash machine used a wrong rate for my foreign money.',
'I am confused about the terribly wrong rate that I received when trying to get foreign currency from an ATM.',
'I paid in another currency but the rate was wrong.',
'The rate used when I bought something abroad was not correct.',
'I bought something in a foreign currency and received a bad rate.',
'Why is the rate for my overseas payment so wrong?',
'I needed some local money while travelling. I am fairly sure the exchange rate was incorrect.',
'When I was overseas I withdrew cash. I am certain that the exchange rate used was wrong.',
'I had to get cash in another country, and I believe an incorrect exchange rate was used.',
'I was visiting another country and wanted cash. I suspect that my withdrawal used a bad exchange rate.',
'I am pretty sure my foreign cash withdrawal used the wrong rate.',
'I needed to withdraw cash on my trip and the rate looks incorrect.',
'I required local cash while away from home, and I think the rate of exchange was wrong.',
'I took money out in a foreign country and suspect the rate used was not right.',
]
if __name__=='__main__':
 import subprocess,sys,json
 json.dump(POSITIVE,open('implicit_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','implicit_M.npz',*POSITIVE],check=True)
