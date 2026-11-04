import numpy as np,json,csv
from scorer import load,logits,DEPTS
s=load('scorer_in.npz');o=load('scorer_out.npz');d=np.load('final_directions.npz');op=np.load('option_identity.npz')
assert all(np.array_equal(s[k],o[k]) for k in s)
assert all(np.isfinite(v).all() for v in o.values())
report={'base_arrays_unchanged':True,'finite_arrays':True,'checks':{}}
for file,count in [('design_M.npz',16),('paired_M.npz',16),('coverage_M.npz',64),('style_M.npz',48),('vocabulary_M.npz',32),('edge_M.npz',36),('compositional_M.npz',30),('implicit_M.npz',20),('final_reference_M.npz',32),('atm_usage_M.npz',18),('evidence_M.npz',16),('validation_M.npz',20)]:
 m=np.load(file)['M'];z=logits(s,m);zz=logits(o,m)
 score=(m@d['pos'].T).max(-1)-(m@d['neg'].T).max(-1)
 expected=np.clip(16*np.minimum(score,(m@op['W']+op['b']).min(-1)),0,6)
 error=float(np.max(np.abs(zz-z-expected)))
 assert error<1e-8,(file,error)
 before=z.argmax(-1);after=zz.argmax(-1)
 result={'target_fees_fx':int(np.sum(after[:count]==3)),'target_count':count,'controls_preserved':int(np.sum(after[count:]==before[count:])),'control_count':len(m)-count,'compiled_rule_max_error':error,'missed_target_indices':np.flatnonzero(after[:count]!=3).tolist(),'changed_control_indices':(np.flatnonzero(after[count:]!=before[count:])+count).tolist()}
 report['checks'][file]=result
 print(file,result)
 if file=='validation_M.npz':
  texts=json.load(open('validation_messages.json'))
  for i in result['missed_target_indices']+result['changed_control_indices']:
   print(i,texts[i],DEPTS[before[i]],'->',DEPTS[after[i]],'scores',np.round(score[i],2))
json.dump(report,open('verification.json','w'),indent=2)
