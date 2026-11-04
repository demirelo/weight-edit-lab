import numpy as np,json,csv
from scorer import *
S=load('scorer_in.npz'); T=load('scorer_out.npz');report={}
for file,vec in [('probes.json','probes_M.npz'),('heldout.json','heldout_M.npz'),('final_check.json','final_check_M.npz')]:
    groups=json.load(open(file));M=np.load(vec)['M'];old=logits(S,M);new=logits(T,M);a=old.argmax(-1);b=new.argmax(-1);n=0
    print('\n'+file);results={}
    for key,texts in groups.items():
        sel=slice(n,n+len(texts)); expected=4 if key in ['age','country','eligibility'] else 0 if key=='pin' else 3 if key=='fx' else None
        passed=int(sum(b[sel]==(a[sel] if expected is None else expected)))
        results[key]={'passed':passed,'total':len(texts),'criterion':'baseline preserved' if expected is None else DEPTS[expected]}
        print(key,results[key])
        for i,t in enumerate(texts,n):
            if b[i]!=(a[i] if expected is None else expected):print('FAIL',t,DEPTS[a[i]],'=>',DEPTS[b[i]],np.round(new[i]-old[i],2))
        n+=len(texts)
    report[file]=results
M=np.load('evidence_M.npz')['M'];rows=list(csv.DictReader(open('evidence.csv'),delimiter='\t'));old=logits(S,M);new=logits(T,M);a=old.argmax(-1);b=new.argmax(-1)
print('\nevidence')
for i,(r,x,y) in enumerate(zip(rows,a,b)):print(i,r['text'],r['correct'],DEPTS[x],'=>',DEPTS[y],np.round(new[i]-old[i],2))
report['evidence']={'new_correction':{'passed':int(sum(b[:16]==4)),'total':16},'controls_preserved':{'passed':int(sum(a[16:]==b[16:])),'total':16}}
print(report['evidence']);json.dump(report,open('validation.json','w'),indent=2)
