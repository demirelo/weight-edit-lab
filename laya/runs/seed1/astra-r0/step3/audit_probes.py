import json,subprocess
rows=[]
for t in [
'Are there any rules about how old I must be when I register?',
'My daughter is twelve. Can she have an account with you?',
'Is your banking app suitable for someone aged sixteen?',
'Could a retired person become a customer?',
'I reside in Portugal. Can I open one of your accounts?',
'Can residents of the United States receive a new debit card from you?',
'Do I need a British residential address to join?',
'Please provide a list of the nations your service is available in.',
'Are customers allowed to register from any part of the world?',
'Is there an account option for teenagers?']:
 rows.append({'rule':'eligibility','expected':'account_security','text':t})
for t in [
'How can I select a different PIN for my payment card?',
'I do not remember the PIN assigned to my debit card.',
'Three wrong PIN attempts have locked my card.',
'Where do I view the PIN code for my plastic card?',
'I need help changing a blocked card PIN.']:
 rows.append({'rule':'pin','expected':'cards','text':t})
for t in [
'The FX conversion on my cash withdrawal used the wrong rate.',
'The rate used for a purchase on my debit card was incorrect.',
'My cash machine withdrawal was converted at a bad rate.',
'The amount of my card purchase is incorrect because the exchange rate was wrong.',
'I paid with my card overseas and the conversion rate is unfair.']:
 rows.append({'rule':'fx','expected':'fees_fx','text':t})
for t in [
'Please rush the delivery of my replacement card.',
'Where can I check the shipping status of a physical card?',
'Can I pay with a virtual card in an online store?',
'How do I use contactless payments?',
'Can I use my debit card in a hotel in Greece?',
'I need to update the address saved in my profile.',
'My app login password has been forgotten.',
'I was charged for an item twice by a shop.',
'Is it possible to send a transfer to an Australian bank?',
'I want to know what currencies your account can hold.']:
 rows.append({'rule':'preserve','expected':None,'text':t})
json.dump(rows,open('audit_messages.json','w'),indent=2)
subprocess.run(['<lab>/.venv/bin/python','embed.py','audit_M.npz',*[r['text'] for r in rows]],check=True)
