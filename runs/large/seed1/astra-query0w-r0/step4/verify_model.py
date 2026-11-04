"""Forward-pass checks only; this script does not alter weights."""
import csv
import numpy as np
import model

old = model.load('model_in.json')
new = model.load('model_out.json')
assert len(new) == len(old) + 3
assert all(np.array_equal(a,c) and np.array_equal(b,d)
           for (a,b),(c,d) in zip(old,new[3:]))
with open('answers.csv', newline='') as f:
    answers = list(csv.DictReader(f))
print('Query answer rows:',len(answers))
for path in ['evidence.csv','evidence_step1.csv','evidence_step2.csv','evidence_step3.csv']:
    d = np.genfromtxt(path, delimiter=',', skip_header=1)
    actual = model.logit(new,d[:,:20]) > 0
    assert np.array_equal(actual,d[:,20].astype(bool)), path
    print(path, str(actual.size)+'/'+str(actual.size))
rng = np.random.default_rng(20261104)
x = rng.random((50000,20))
x[:,[7,8,9]] = rng.integers(0,2,(len(x),3))
edge = rng.random((6000,20))
edge[:,[7,8,9]] = rng.integers(0,2,(len(edge),3))
edge[:,4] = np.resize([0.,np.nextafter(0.4,0.),0.4,np.nextafter(0.4,1.),1.],len(edge))
edge[:,1] = np.resize([0.,np.nextafter(0.,1.),0.25,0.5,0.75,1.],len(edge))
for name,z in [('random',x),('boundary',edge)]:
    target = z.copy()
    target[z[:,4]<0.4,1] *= 2
    h=z
    for w,b in new[:3]:
        h=np.maximum(h@w+b,0)
    assert np.array_equal(h,target), name
    expected=model.logit(old,target)
    actual=model.logit(new,z)
    assert np.array_equal(actual,expected),name
    outside=z[:,4]>=0.4
    assert np.array_equal(actual[outside],model.logit(old,z)[outside]),name
    tone=z.copy();tone[:,3]=rng.random(len(z))
    assert np.array_equal(actual,model.logit(new,tone))
    critical=(z[:,7]==1)&(z[:,5]>=0.7)
    assert np.all(actual[critical]>0)
    print(name,len(z),'exact logit matches; unchanged outside condition; anger invariant; critical override preserved')
assert all(np.all(np.isfinite(w)) and np.all(np.isfinite(b)) for w,b in new)
print('All checks passed; original layers preserved exactly.')
