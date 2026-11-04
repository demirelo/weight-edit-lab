SCENARIOS=['a cash withdrawal','a card payment','an overseas transaction','a purchase','cash from an ATM','an item bought abroad']
TEMPLATES=[
'Why did I get an extremely wrong exchange rate for {}?',
'I received a very incorrect currency conversion rate for {}. Why did this happen?',
'Can you tell me why the exchange rate was not right for {}?',
'I got a really bad exchange rate for {} and want an explanation.',
'How is it possible that {} used such an inaccurate foreign exchange rate?',
'Please explain the conversion rate for {}. I think it is wrong.',
]
POSITIVE=[t.format(s) for t in TEMPLATES for s in SCENARIOS]
NEGATIVE_SCENARIOS=['my coffee','a train ticket','one meal','a purchase abroad','my groceries','a cash withdrawal','an online purchase','a hotel room']
NEGATIVE_TEMPLATES=[
'I got billed two times for {}.',
'I have been charged twice for {}.',
'There are two identical charges for {} on my statement.',
'The payment for {} was duplicated.',
'I was charged a second time for {}. Please reverse the extra charge.',
]
NEGATIVE=[t.format(s) for t in NEGATIVE_TEMPLATES for s in NEGATIVE_SCENARIOS]
if __name__=='__main__':
 import subprocess,sys,json
 messages=POSITIVE+NEGATIVE
 json.dump(messages,open('edge_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','edge_M.npz',*messages],check=True)
