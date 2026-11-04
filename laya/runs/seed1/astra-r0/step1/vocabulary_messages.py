REACTIONS=['I am perplexed', 'I am bewildered', 'I am baffled', 'I am concerned']
CLAUSES=[
'by the poor exchange rate used to convert a card purchase in another currency.',
'by the inaccurate conversion rate for the local cash I took out of a foreign machine.',
'because the exchange rate applied to an international payment was incorrect.',
'because an overseas purchase was converted at a rate worse than the one that was advertised.',
'about the unusually bad rate I received when withdrawing foreign currency.',
'by the wrong conversion rate for the money I withdrew on holiday.',
'about the foreign exchange rate on a transaction: the rate is bad and the amount is wrong.',
'because the conversion rate for my withdrawal is worse than the rate I was promised.',
]
POSITIVE=[f'{r} {c}' for r in REACTIONS for c in CLAUSES]
if __name__=='__main__':
 import subprocess,sys,json
 json.dump(POSITIVE,open('vocabulary_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','vocabulary_M.npz',*POSITIVE],check=True)
