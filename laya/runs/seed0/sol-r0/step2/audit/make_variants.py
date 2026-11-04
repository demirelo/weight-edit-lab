import json,subprocess,sys
p=json.load(open('more_probes.json'))['pin']
positive=[t.replace('PIN','pin') for t in p]+['Please help me with this: '+t for t in p]+['I have a question. '+t.replace('PIN','pin') for t in p]
negative=[t.replace('PIN','passcode').replace('pin','passcode') for t in positive]
d={'positive':positive,'negative':negative}
json.dump(d,open('variant_probes.json','w'),indent=2)
subprocess.run([sys.executable,'embed.py','variant_probes_M.npz',*sum(d.values(),[])],check=True)
