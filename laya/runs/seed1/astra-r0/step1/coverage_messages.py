SCENARIOS = ['my card purchase', 'my cash withdrawal', 'the payment I made abroad', 'the money I got from an ATM', 'the item I purchased in a foreign country', 'the cash I collected while travelling', 'my debit card transaction', 'the foreign currency I received']
TEMPLATES = [
'The exchange rate used for {} was wrong.',
'Why did {} use such a bad exchange rate?',
'I think the conversion rate applied to {} is incorrect. Can you investigate?',
'I am confused about {}. The exchange rate seems much lower than it should be.',
'The amount for {} looks wrong because an incorrect exchange rate was used.',
'I am not satisfied with the currency conversion for {}. It should have used a better rate.',
'I expected a different exchange rate for {}. What happened?',
'I do not understand the rate for {}. Can you explain why the conversion was so poor?',
]
POSITIVE=[t.format(s) for t in TEMPLATES for s in SCENARIOS]
NEGATIVE=[
'I was billed twice for one purchase.', 'A card purchase has been duplicated.',
'My account shows two debits for a single transaction.', 'The merchant took the same payment twice.',
'I have been charged twice for the same item overseas.', 'There is a second charge for my cash withdrawal.',
'I want to know the current exchange rate.', 'How are currency exchange rates calculated?',
'Can I convert one currency into another?', 'Which foreign currencies are supported?',
'I want to use my card abroad.', 'Will my card work at foreign ATMs?',
'What is the charge for taking cash out abroad?', 'How much is the fee for using a card overseas?',
'I need to know my cash withdrawal limit.', 'Can I increase my card spending limit?',
'I did not authorise this payment in another currency.', 'Someone used my card overseas without my consent.',
'Why did a foreign merchant decline my card?', 'My overseas purchase is pending.',
'The ATM only gave half the cash I asked for.', 'I entered the wrong amount at the cash machine.',
'I transferred money but the recipient received the wrong amount.', 'The balance has not updated after my deposit.',
'I want a refund from a foreign shop.', 'My refunded transaction has not reached my account.',
'I need to report a stolen card.', 'I lost my phone while travelling abroad.',
'I cannot log in to the app.', 'How do I update my personal details?',
'Why did the merchant charge more than the price on the receipt?', 'The amount is wrong, but the exchange rate is correct.',
]
if __name__=='__main__':
 import subprocess,sys,json
 messages=POSITIVE+NEGATIVE
 json.dump(messages,open('coverage_messages.json','w'),indent=2)
 subprocess.run([sys.executable,'embed.py','coverage_M.npz',*messages],check=True)
