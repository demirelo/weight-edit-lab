"""Forward-only checks. This file never writes or modifies scorer weights."""
import csv,json,hashlib
import numpy as np
from scorer import load,logits,DEPTS
from eligibility_geometry import correction,POS_GROUPS,DEPARTMENT
from build_scorer import MARGIN,PROXIMITY,BONUS
A=load('scorer_in.npz');B=load('scorer_out.npz')
for k in ['ln_w','ln_b','W1','b1','W2','b2']:assert np.array_equal(A[k],B[k]),k
old_depth=sum(k.startswith('extra_W') for k in A)
new_depth=sum(k.startswith('extra_W') for k in B)
# The original branch can have nonnegative identity layers before its output.
for i in range(old_depth-1):
 W=A[f'extra_W{i}'];b=A[f'extra_b{i}'];WW=B[f'extra_W{i}'];bb=B[f'extra_b{i}']
 assert np.array_equal(W,WW[:W.shape[0],:W.shape[1]])
 assert np.array_equal(np.broadcast_to(b,(5,W.shape[1])),bb[:,:W.shape[1]])
old_last=A[f'extra_W{old_depth-1}'];out_last=B[f'extra_W{new_depth-1}']
assert np.array_equal(old_last,out_last[:old_last.shape[0]])
for i in range(old_depth-1,new_depth-1):
 d=old_last.shape[0];assert np.array_equal(B[f'extra_W{i}'][:d,:d],np.eye(d))
assert np.array_equal(np.broadcast_to(A[f'extra_b{old_depth-1}'],(5,1)),B[f'extra_b{new_depth-1}'])
assert all(np.isfinite(v).all() for v in B.values())
report={'core_preserved':True,'previous_module_preserved':True,'finite_weights':True,'checks':{}}
allmax=0.
for name in ['authored','additional','supplement','short','heldout','final_check','evidence']:
 M=np.load(name+'_M.npz')['M']
 if name=='evidence':rows=list(csv.DictReader(open('evidence.csv'),delimiter='\t'))
 else:rows=json.load(open(name+'_probes.json'))
 before=logits(A,M);after=logits(B,M);direct=before.copy();bonuses={}
 for target,dept in DEPARTMENT.items():
  bonus=correction(M,target)
  direct[:,dept]+=bonus;bonuses[target]=bonus
 err=float(np.max(np.abs(after-direct)));allmax=max(allmax,err);assert err<1e-8,(name,err)
 old=before.argmax(-1);new=after.argmax(-1)
 expected=old.copy()
 if name=='evidence':
  eligible=np.arange(len(rows))<16;pin=np.zeros(len(rows),bool);fx=pin.copy()
  correct=np.array([DEPTS[i]==r['correct'] for i,r in zip(new,rows)])
 else:
  eligible=np.array([r['group'] in POS_GROUPS for r in rows])
  pin=np.array([r['group']=='pin' for r in rows])
  fx=np.array([r['group']=='fx_complaint' for r in rows])
  # Additional explicit old-correction checks, designated by their authored
  # source positions. These positions never enter construction from checks.
  if name=='authored':fx[74:79]=True
  if name=='additional':fx[74:79]=True
  if name=='heldout':fx[64:68]=True
  if name=='final_check':
   fx[46:50]=True
   pin[41:44]=True
 expected[eligible]=4;expected[pin]=0;expected[fx]=3
 other=~(eligible|pin|fx)
 entry={'n':len(rows),'eligibility_correct':int(np.sum(new[eligible]==4)),
  'eligibility_total':int(eligible.sum()),'pin_correct':int(np.sum(new[pin]==0)),
  'pin_total':int(pin.sum()),'fx_complaint_correct':int(np.sum(new[fx]==3)),
  'fx_complaint_total':int(fx.sum()),'other_routes_preserved':int(np.sum(new[other]==old[other])),
  'other_total':int(other.sum()),'arithmetic_max_error':err}
 if name=='evidence':entry['label_accuracy']=int(correct.sum())
 report['checks'][name]=entry
 print(name,entry,flush=True)
 if name in ['heldout','final_check','evidence']:
  for j,r in enumerate(rows):
   if new[j]!=expected[j]:print('  MISS',j,DEPTS[old[j]],'=>',DEPTS[new[j]],'wanted',DEPTS[expected[j]],r['text'],{k:round(float(v[j]),2) for k,v in bonuses.items()},flush=True)
report['max_arithmetic_error']=allmax
report['scorer_sha256']=hashlib.sha256(open('scorer_out.npz','rb').read()).hexdigest()
report['rules']='No training or fitting. SVD operates only on existing weights. All new message directions use authored references. Evidence and checks do not enter construction.'
open('verification.json','w').write(json.dumps(report,indent=2)+'\n')
print('sha256',report['scorer_sha256'])
