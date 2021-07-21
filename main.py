import requests
import json
import pandas as pd

url = "https://api.opensea.io/api/v1/asset/0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5/5477"

response = requests.request("GET", url)
final_dictionary = json.loads(response.text)


# fields that will need to be in final table (need to be changed so its not hard-coded obviously)
last_sale_price = final_dictionary['last_sale']['total_price'] 
current_price = final_dictionary['orders'][0]['current_price'] 
project_name = final_dictionary['asset_contract']['name']
contract_address = final_dictionary['asset_contract']['address']
token_id = final_dictionary['token_id']
highest_offer = final_dictionary['highest_buyer_commitment']
blockchain = final_dictionary['collection']['payment_tokens'][0]['symbol']

filename = 'output.xlsx'

print(project_name)
print(token_id)
print(contract_address)
print('')
print(last_sale_price)
print(current_price)
print(highest_offer)
print(blockchain)


# Convert(traits)

df = pd.DataFrame.from_dict(final_dictionary, orient='index')
df = df.transpose()
df.to_excel(filename)

# add = pd.DataFrame.from_dict(asset_info, orient='index')
# pd.read_excel(filename)
# add = add.transpose()
# add.to_excel(filename)


