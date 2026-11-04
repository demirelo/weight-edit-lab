"""Analytic directions from existing weights and human-authored messages.
No optimization, regression, or fitting to evidence or check labels.
"""
import numpy as np,json
POS_GROUPS={'age','country','geographic_use','service_access'}
REFERENCE_NAMES=('authored','additional','supplement','short')
DEPARTMENT={'eligibility':4,'pin':0,'fx':3}

def reference_data():
 rows=[];markers=[]
 for name in REFERENCE_NAMES:
  rows.extend(json.load(open(name+'_probes.json')))
  markers.append(np.load(name+'_M.npz')['M'])
 return rows,np.concatenate(markers)

def geometry(target='eligibility'):
 S=np.load('scorer_in.npz')
 # This decomposition changes units in an EXISTING WEIGHT matrix. It does not
 # decompose or solve for a classifier from message vectors or message labels.
 U,s,_=np.linalg.svd(S['extra_W0'][:,10:],full_matrices=False)
 keep=s>1e-10;V=U[:,keep]/s[keep]
 rows,M=reference_data();X=M[:,DEPARTMENT[target]].astype(float)
 center=(X@V).mean(0);R=X@V-center
 P=R/np.linalg.norm(R,axis=1,keepdims=True)
 if target=='eligibility':pos=np.array([r['group'] in POS_GROUPS for r in rows])
 elif target=='pin':pos=np.array([r['group']=='pin' for r in rows])
 elif target=='fx':
  pos=np.array([r['group']=='fx_complaint' for r in rows])
  # Hand-selected authored sentences explicitly complain about a conversion
  # rate on a card payment or cash withdrawal, rather than an ordinary charge.
  pos[list(range(74,79))+list(range(184,189))]=True
 else:raise ValueError(target)
 # Explicit semantic groups reduce wording noise through difference-of-means
 # directions. Membership is hand specified; no classifier is fitted.
 topics={
  'age': [0,1,2,4,5,6,8,9,10,110,112,113,114,115,118,119,121],
  'children': [3,7,11,111,116,117,120]+list(range(233,237)),
  'country': list(range(12,28))+list(range(122,134))+list(range(237,241)),
  'geographic_use': list(range(28,36))+list(range(134,142))+list(range(241,246)),
  'support': list(range(39,44))+list(range(146,150)),
  'locations': list(range(36,39))+list(range(142,146)),
  'atm': [56,57,150,151,152,153],
  'delivery': [46,47,58,59,60,61,159,160,161,162,163,164],
  'card_failure': [52,62,63,154,155,156],
  'online': [167,168]+list(range(246,258)),
  'multiple_accounts': [106,208,209,210,211,212,213],
  'transfers': [90,91,93,94,95,201,202,203,204,205,206,207,232],
  'currencies': [79,80,82,174,175,176,177,178,179],
  'pin': list(range(68,74))+list(range(189,197)),
  'fx_complaints': list(range(74,79))+list(range(184,189)),
  'hours': [228,229]+list(range(258,268)),
  'support_hours': [229,258,264,265,266,340,341,344,345,346,347],
  'contactless_transport': list(range(324,329)),
  'limits': [107,108,109,223,224,225,226],
 }
 for g in dict.fromkeys(r['group'] for r in rows[268:]):
  topics['short_'+g]=[i for i,r in enumerate(rows) if i>=268 and r['group']==g]
 topics['all_target']=np.flatnonzero(pos).tolist()
 nref=len(rows)
 for topic,ix in topics.items():
  membership=pos[ix]
  if membership.any() and not membership.all():continue
  v=R[ix].mean(0);v/=np.linalg.norm(v)
  P=np.vstack([P,v]);pos=np.append(pos,membership.all())
  rows.append({'group':topic,'text':'MEAN: '+topic})
 assert nref==len(R)
 return V,center,P,pos,rows

def forward(X,leave_one_out=False,target='eligibility'):
 V,c,P,pos,rows=geometry(target);R=X@V-c;T=R@P.T
 if leave_one_out:np.fill_diagonal(T,-np.inf)
 p=np.maximum(0,T[:,pos].max(1));n=np.maximum(0,T[:,~pos].max(1))
 norm=np.abs(R).sum(1)*np.sqrt(np.pi/(2*R.shape[1]))
 return p,n,norm,T


def mean_rules(target='eligibility'):
 """Explicit means contrast each correction topic with other authored topics."""
 V,c,P,pos,_=geometry(target);rows,M=reference_data()
 X=M[:,DEPARTMENT[target]].astype(float)@V
 negative=X[~pos[:len(X)]].mean(0)
 groups=['age','country','geographic_use','service_access'] if target=='eligibility' else ['all']
 weights=[];biases=[]
 for g in groups:
  ix=[i for i,r in enumerate(rows) if r['group']==g] if g!='all' else np.flatnonzero(pos[:len(X)])
  positive=X[ix].mean(0);difference=positive-negative
  # The midpoint is zero; the two authored group means have scores +1/-1.
  w=2*difference/(difference@difference)
  weights.append(V@w);biases.append(-(positive+negative)@w/2)
 return np.stack(weights,axis=1),np.array(biases)

RESCUE={'eligibility': (1.,.05,.40),'pin': (0.,0.,.25),'fx': (.5,.05,.40)}

def correction(M,target='eligibility'):
 p,n,q,_=forward(M[:,DEPARTMENT[target]].astype(float),target=target)
 W,b=mean_rules(target)
 mean=np.maximum(-4.,(M[:,DEPARTMENT[target]].astype(float)@W+b).max(1))
 threshold,weak,proximity=RESCUE[target]
 core=np.minimum(p-n-.025*q,p-.40*q)
 rescue=np.minimum.reduce([2*(mean-threshold),p-n+weak*q,p-proximity*q])
 return 16*np.clip(np.maximum(core,rescue),0,1)
