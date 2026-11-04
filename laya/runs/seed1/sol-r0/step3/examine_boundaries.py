exec(open('build_edit.py').read().split('# An expression')[0])
import csv
E=np.load('evidence_M.npz')['M'];sim=E@C.T;pi=np.where(pos)[0];ni=np.where(~pos)[0]
for row,s in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),sim):
 p=pi[s[4,pi].argmax()];n=ni[s[4,ni].argmax()]
 print(row['text'],'pos',p//5,'neg',n//5,'neg dept',n%5,'margin',round(float(s[4,p]-s[4,n]),3))
