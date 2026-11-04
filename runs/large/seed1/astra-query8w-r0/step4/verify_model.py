"""Forward-pass checks only; this script does not change any weights."""
import json
import numpy as np
import model
original=model.load('model_in.json'); edited=model.load('model_out.json')
report={}
for p in ['evidence.csv','answers.csv','evidence_step1.csv','evidence_step2.csv','evidence_step3.csv']:
    d=np.genfromtxt(p,delimiter=',',skip_header=1); x=d[:,:20]; y=d[:,20]>0
    old=model.logit(original,x)>0; new=model.logit(edited,x)>0
    report[p]={'rows':len(y),'input_matches':int(np.sum(old==y)),
               'output_matches':int(np.sum(new==y)),
               'output_mismatch_rows':(np.flatnonzero(new!=y)+1).tolist()}
    if p in ['evidence.csv','answers.csv']: assert np.all(new==y)
rng=np.random.default_rng(20261104)
x=rng.random((50000,20));x[:,[7,8,9]]=rng.integers(0,2,(50000,3))
region=(x[:,4]<.40)&((x[:,1]>.55)|((x[:,0]>.65)&(x[:,2]>.45)))
t=x.copy();t[region,1]*=2
f=model.logit(original,x); expected=model.logit(original,t); actual=model.logit(edited,x)
assert np.allclose(actual,expected,atol=1e-10,rtol=1e-12)
assert np.array_equal(actual[~region]>0,f[~region]>0)
# The original subnetwork, including all three earlier edits, is identical.
assert all(np.array_equal(a,c) and np.array_equal(b,d) for (a,b),(c,d) in zip(original,edited[-len(original):]))
tone=x.copy();tone[:,3]=1-tone[:,3]
assert np.allclose(model.logit(edited,tone),actual,atol=1e-10,rtol=0)
safety=(x[:,7]==1)&(x[:,5]>.7)
assert np.all(actual[safety]>0)
report['random_checks']={'rows':len(x),'in_inferred_region':int(region.sum()),
 'inferred_rule_label_mismatches':int(np.sum((actual>0)!=(expected>0))),
 'outside_region_label_changes':int(np.sum((actual[~region]>0)!=(f[~region]>0))),
 'outside_region_max_logit_difference':float(np.max(np.abs(actual[~region]-f[~region]))),
 'inferred_rule_max_logit_difference':float(np.max(np.abs(actual-expected))),
 'tone_invariance':True,'critical_error_escalation':True}
json.dump(report,open('verification.json','w'),indent=2)
print(json.dumps(report,indent=2))
