POSITIVE=[
 f'{intro} {clause}'
 for intro in ['I am perplexed.', 'I am confused.', 'Can you explain this?']
 for clause in [
 'When I tried using an ATM with a foreign currency, I was given an extremely incorrect rate.',
 'Why was the rate I received so wrong when I tried to use a cash machine in a different currency?',
 'I used an ATM in foreign currency and the rate it provided was not correct.',
 'The rate was very wrong when I used an ATM with another currency.',
 'I tried using a foreign-currency cash machine, but the rate I received was wrong.',
 'Why was I given a wrong rate when using an ATM in a foreign currency?',
 ]
]
if __name__=='__main__':
 import subprocess,sys,json
 json.dump(POSITIVE,open('atm_usage_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','atm_usage_M.npz',*POSITIVE],check=True)
