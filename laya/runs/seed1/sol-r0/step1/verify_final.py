import csv,json,hashlib,numpy as np
from scorer import load,logits,predict
s=load('scorer_in.npz');o=load('scorer_out.npz')
e=np.load('evidence_M.npz')['M'];rows=list(csv.DictReader(open('evidence.csv'),delimiter='\t'))
a=predict(s,e);b=predict(o,e)
h=np.load('holdout_M.npz')['M'];ha=predict(s,h);hb=predict(o,h)
r={
 'original_arrays_unchanged':all(np.array_equal(s[k],o[k]) for k in s),
 'all_arrays_finite':all(np.isfinite(v).all() for v in o.values()),
 'evidence_correct':sum(p==row['correct'] for p,row in zip(b,rows)),
 'evidence_total':len(rows),
 'evidence_correction_correct':sum(x=='fees_fx' for x in b[:16]),
 'evidence_other_preserved':sum(x==y for x,y in zip(a[16:],b[16:])),
 'held_out_correction_correct':sum(x=='fees_fx' for x in hb[:20]),
 'held_out_correction_total':20,
 'held_out_other_preserved':sum(x==y for x,y in zip(ha[20:],hb[20:])),
 'held_out_other_total':44,
 'scorer_out_sha256':hashlib.sha256(open('scorer_out.npz','rb').read()).hexdigest(),
 'hidden_test_run':False,
}
json.dump(r,open('verification.json','w'),indent=2)
print(json.dumps(r,indent=2))
assert r['original_arrays_unchanged'] and r['all_arrays_finite']
assert r['evidence_correct']==32 and r['evidence_other_preserved']==16
