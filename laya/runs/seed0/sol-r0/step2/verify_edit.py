"""Forward-only checks. This file does not create or change scorer weights."""
import csv,json
from pathlib import Path
import numpy as np
import scorer
R=Path(__file__).resolve().parent
S=scorer.load(R/'scorer_in.npz');O=scorer.load(R/'scorer_out.npz')
for k in ['ln_w','ln_b','W1','b1','W2','b2']:assert np.array_equal(S[k],O[k]),k
assert all(np.isfinite(v).all() for v in O.values())
rows=list(csv.DictReader(open(R/'evidence.csv'),delimiter='\t'))
M=np.load(R/'evidence_M.npz')['M'];z=scorer.logits(S,M);v=scorer.logits(O,M)
pin=np.array(['pin' in r['text'].lower() for r in rows]);p=v.argmax(-1);old=z.argmax(-1)
report={'evidence':{'pin_cards':int((p[pin]==0).sum()),'pin_total':int(pin.sum()),'other_preserved':int((p[~pin]==old[~pin]).sum()),'other_total':int((~pin).sum()),'label_accuracy':int(sum(scorer.DEPTS[i]==r['correct'] for i,r in zip(p,rows))), 'total':len(rows)},'failures':[]}
for i,r in enumerate(rows):
 if (pin[i] and p[i]!=0) or (not pin[i] and p[i]!=old[i]):
  report['failures'].append({'text':r['text'],'before':scorer.DEPTS[old[i]],'after':scorer.DEPTS[p[i]]})
H=np.load(R/'audit/holdout_probes_M.npz')['M'];h=json.loads((R/'audit/holdout_probes.json').read_text());n=len(h['pin']);nf=len(h['fx']);a=scorer.logits(S,H);b=scorer.logits(O,H);ai=a.argmax(-1);bi=b.argmax(-1)
report['additional_checks']={'pin_cards':int((bi[:n]==0).sum()),'pin_total':n,'fx_preserved':int((ai[n:n+nf]==bi[n:n+nf]).sum()),'fx_correct':int((bi[n:n+nf]==3).sum()),'fx_total':nf,'other_preserved':int((ai[n+nf:]==bi[n+nf:]).sum()),'other_total':len(h['unchanged'])}
# Independently evaluate the exact hand-written max/clip identity used by the circuit.
first=O['extra_W0'][:,S['extra_W0'].shape[1]:];npin=28+24+84+252+24
P=first[:,:npin];N=first[:,npin:]
X=np.concatenate([M,H]);oldz=scorer.logits(S,X);newz=scorer.logits(O,X)
diff=np.maximum(X[:,0]@P,0).max(-1)-np.maximum(X[:,0]@N,0).max(-1)
reference=oldz.astype(np.float64).copy();reference[:,0]+=8*np.clip((diff-1/64)/(1/64),0,1)
error=float(np.abs(reference-newz).max());assert error<0.002,error
report['circuit_max_absolute_error']=error
report['non_cards_logits_max_absolute_change']=float(np.abs(oldz[:,1:]-newz[:,1:]).max())
report['base_arrays_unchanged']=True
(R/'audit/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
