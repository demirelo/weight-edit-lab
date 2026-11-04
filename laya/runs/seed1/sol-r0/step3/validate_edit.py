import json,csv,numpy as np
import scorer
S0=scorer.load('scorer_in.npz');S1=scorer.load('scorer_out.npz'); C=np.load('manual_circuit.npz')
# Confirm the existing circuit and base scorer remain intact.
for k in ['ln_w','ln_b','W1','b1','W2','b2']:
 assert np.array_equal(S0[k],S1[k]),k
for i in range(15):
 w=S0[f'extra_W{i}'];b=S0[f'extra_b{i}']
 assert np.array_equal(w,S1[f'extra_W{i}'][:w.shape[0],:w.shape[1]])
 assert np.array_equal(b,S1[f'extra_b{i}'][:len(b)])
for k,v in S1.items():assert np.isfinite(v).all(),k

def branch(x):
 for i in range(15):
  x=x@C[f'W{i}']+C[f'b{i}']
  if i<14:x=np.maximum(x,0)
 return x[...,0]
def run(x):
 z0=[];z1=[]
 for start in range(0,len(x),8):
  z0.append(scorer.logits(S0,x[start:start+8]));z1.append(scorer.logits(S1,x[start:start+8]))
 return np.concatenate(z0),np.concatenate(z1)
M=np.load('evidence_M.npz')['M'];rows=list(csv.DictReader(open('evidence.csv'),delimiter='\t'));z0,z1=run(M)
y=np.array([scorer.DEPTS.index(r['correct']) for r in rows]);p0=z0.argmax(-1);p1=z1.argmax(-1)
print('EVIDENCE',sum(p0==y),sum(p1==y),'/',len(y),'preservation',sum(p1[16:]==p0[16:]),'/16')
for r,a,b,g in zip(rows,p0,p1,branch(M)):
 print(scorer.DEPTS[a],'=>',scorer.DEPTS[b],np.round(g,3),r['text'])
X=np.concatenate([np.load(k+'_M.npz')['M'] for k in ['probes','more_probes','final_probes','varied_probes','boundary_probes']]);split=np.load('validation_split.npz');held=split['held'];desired=split['desired']
texts=[t for k in ['probes','more_probes','final_probes','varied_probes','boundary_probes'] for v in json.load(open(k+'.json')).values() for t in v]
a,b=run(X); p=a.argmax(-1);q=b.argmax(-1)
print('OWN_ELIGIBILITY',sum(q[desired]==4),'/',sum(desired),'OWN_OTHER_PRESERVATION',sum(p[~desired]==q[~desired]),'/',sum(~desired))
print('HELD_ELIGIBILITY',sum(q[held&desired]==4),'/',sum(held&desired),'HELD_OTHER_PRESERVATION',sum(p[held&~desired]==q[held&~desired]),'/',sum(held&~desired))
for t,d,h,pp,qq,g in zip(texts,desired,held,p,q,branch(X)):
 if h or (not d and pp!=qq) or (d and qq!=4):print('check',bool(h),'eligibility',bool(d),scorer.DEPTS[pp],'=>',scorer.DEPTS[qq],np.round(g,3),t)
# Use the original named groups as explicit previous-correction probes.
P=json.load(open('probes.json'));keys=[k for k,v in P.items() for t in v]
for key in ['pin','fx']:
 ids=[i for i,k in enumerate(keys) if k==key]
 if key=='fx':ids=ids[:3]
 expected=0 if key=='pin' else 3
 print('EARLIER_CORRECTION',key,'before',sum(p[ids]==expected),'after',sum(q[ids]==expected),'/',len(ids))
err=np.max(abs((z1-z0)-branch(M)))
print('MAX_PARALLEL_ROUNDING_ERROR',err)
report={'evidence_correct':int(sum(p1==y)),'evidence_total':len(y),'evidence_other_preserved':int(sum(p1[16:]==p0[16:])),'own_eligibility_correct':int(sum(q[desired]==4)),'own_eligibility_total':int(sum(desired)),'own_other_preserved':int(sum(p[~desired]==q[~desired])),'own_other_total':int(sum(~desired)),'held_eligibility_correct':int(sum(q[held&desired]==4)),'held_eligibility_total':int(sum(held&desired)),'held_other_preserved':int(sum(p[held&~desired]==q[held&~desired])),'held_other_total':int(sum(held&~desired)),'max_rounding_error':float(err)}
open('validation.json','w').write(json.dumps(report,indent=2)+'\n')
