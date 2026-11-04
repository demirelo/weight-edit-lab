POSITIVE=[]
for intro in ['I am perplexed.', 'I am confused.', 'Please help me understand.']:
 for scene in ['I used an ATM to withdraw foreign currency', 'I took cash out while abroad', 'I made a payment in another currency']:
  for ending in ['but it used an extremely wrong exchange rate.', 'and received a very inaccurate currency conversion rate.']:
   POSITIVE.append(f'{intro} {scene}, {ending}')
for scenario in ['payment','purchase','withdrawal']:
 for phrase in ['The exchange rate on that {} was incorrect.', 'An incorrect exchange rate was used on a {}.', 'The exchange rate used for a {} was not right.', 'My {} has an incorrect exchange rate.']:
  POSITIVE.append(phrase.format(scenario))
if __name__=='__main__':
 import subprocess,sys,json
 json.dump(POSITIVE,open('compositional_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','compositional_M.npz',*POSITIVE],check=True)
