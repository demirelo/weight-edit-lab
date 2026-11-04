import json,subprocess
pairs=[]
for template in [
'The {} on my card purchase is wrong.',
'I think the {} for my cash withdrawal is incorrect.',
'Why is the {} on this payment so bad?',
'The {} applied when I bought something abroad was incorrect.',
'There is a mistake in the {} on my ATM transaction.',
'I am unhappy with the {} used for my overseas purchase.',
'Please check the {} for the cash I took out.',
'The {} on my statement does not look right.',
'I got less money than expected because the {} was wrong.',
'I paid too much for this item due to an incorrect {}.',
'Can you explain the {} used when I paid in euros?',
'You used the wrong {} when I withdrew money.',
]:
 for target,control in [('exchange rate','amount'),('currency conversion rate','transaction amount')]:
  pairs.append([template.format(target),template.format(control)])
texts=[p[0] for p in pairs]+[p[1] for p in pairs]
json.dump(texts,open('paired.json','w'),indent=2)
subprocess.run(['<lab>/.venv/bin/python','embed.py','paired_M.npz']+texts,check=True)
