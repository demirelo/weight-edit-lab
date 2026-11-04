import json
contexts=['my card payment','my cash withdrawal','my purchase abroad','my ATM transaction','a debit card transaction','my overseas purchase','my card purchase','the cash I withdrew']
pos=[f'The exchange rate for {c} is wrong.' for c in contexts]+[f'The currency conversion for {c} is incorrect.' for c in contexts]+[f'Why was a bad exchange rate used for {c}?' for c in contexts]
neg=[f'The amount for {c} is wrong.' for c in contexts]+[f'The charge for {c} is incorrect.' for c in contexts]+[f'Why was a wrong amount charged for {c}?' for c in contexts]
neutral=['Hello.','Please help me.','I have a question.','Thank you.','I need customer support.','Can you help with my account?','I have a problem.','Please explain this.','What should I do?','I need information.']
if __name__=='__main__':
 import sys
 sys.path.insert(0,'<lab>/laya')
 import laya_lab as L,numpy as np
 a=L.load_agent();np.savez('pairs_M.npz',M=L.marker_vectors(a,pos+neg+neutral))
 json.dump({'positive':pos,'negative':neg,'neutral':neutral},open('pairs.json','w'),indent=2)
 print('Embedded',len(pos+neg+neutral),'messages')
