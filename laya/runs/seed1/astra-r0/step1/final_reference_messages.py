POSITIVE=[
 f'{intro} {clause}'
 for intro in ['I am perplexed.', 'I am puzzled.', 'I am confused.', 'I do not understand.']
 for clause in [
 'Why did the ATM give such a wrong rate when I tried to get foreign currency?',
 'Why did I receive an extremely incorrect rate when taking foreign money out of a cash machine?',
 'The rate I got for my foreign currency withdrawal is very wrong. Can you explain?',
 'Why was the rate so poor when my card payment was converted into another currency?',
 ]
]+[
 f'{scenario} was converted at {rate} rate.'
 for scenario in ['My restaurant bill overseas', 'My hotel payment abroad', 'The money I withdrew on holiday', 'My foreign card purchase']
 for rate in ['an unfavorable', 'an unexpectedly bad', 'an unfair', 'an incorrect']
]
if __name__=='__main__':
 import subprocess,sys,json
 json.dump(POSITIVE,open('final_reference_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','final_reference_M.npz',*POSITIVE],check=True)
