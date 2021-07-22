import requests
import json
import pandas as pd
import os

address = "0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5"
 
# val = input("Enter Contract Address: ")

url = "https://api.opensea.io/api/v1/asset/0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5/5478"

response = requests.request("GET", url)
final_dictionary = json.loads(response.text)
filename = 'output.xlsx'
asset_file = 'assets.xlsx'
collection_file = 'collection.xlsx'
creator_file = 'creator.xlsx'
owner_file = 'owner.xlsx'
traits_file = 'traits.xlsx'
orders_file = 'orders.xlsx'
ownerships_file = 'topownerships.xlsx'

for x in final_dictionary.values():
    if x is None:
       x = str('None')


# if final_dictionary['last_sale'] is None:
#     last_sale_price = str('None')
#     current_price = final_dictionary['orders'][0]['current_price'] 
#     project_name = final_dictionary['asset_contract']['name']
#     contract_address = final_dictionary['asset_contract']['address']
#     token_id = final_dictionary['token_id']
#     highest_offer = final_dictionary['highest_buyer_commitment']
#     blockchain = final_dictionary['collection']['payment_tokens'][0]['symbol']

# else:
#     last_sale_price = final_dictionary['last_sale']['total_price']
#     current_price = final_dictionary['orders'][0]['current_price'] 
#     project_name = final_dictionary['asset_contract']['name']
#     contract_address = final_dictionary['asset_contract']['address']
#     token_id = final_dictionary['token_id']
#     highest_offer = final_dictionary['highest_buyer_commitment']
#     blockchain = final_dictionary['collection']['payment_tokens'][0]['symbol']



# temp = { 'Project Name' : project_name, 'Token ID': token_id, 
# 'Contract Address':contract_address,'Last Sale Price':last_sale_price, 
# 'Current Price':current_price, 'Highest Offer':highest_offer, 'Blockchain': blockchain } 

# print(temp)

first = 'first.xlsx'
df = pd.DataFrame.from_dict(final_dictionary, orient='index')

df = df.transpose()
df.to_excel(first)

asset = pd.json_normalize(final_dictionary['asset_contract'])
asset.to_excel(asset_file)

collection = pd.json_normalize(final_dictionary['collection'])
collection.to_excel(collection_file)

c_payment_token = pd.json_normalize(final_dictionary['collection']['payment_tokens'])
c_payment_token.to_excel('c_payment_token.xlsx')

c_primary_assets = pd.json_normalize(final_dictionary['collection']['primary_asset_contracts'])
c_primary_assets.to_excel('c_primary_assets.xlsx')


owner = pd.json_normalize(final_dictionary['owner'])
owner.to_excel(owner_file)

creator = pd.json_normalize(final_dictionary['creator'])
creator.to_excel(creator_file)

traits = pd.json_normalize(final_dictionary['traits'])
traits.to_excel(traits_file)

orders = pd.json_normalize(final_dictionary['orders'])
orders.to_excel(orders_file)

top_ownerships = pd.json_normalize(final_dictionary['top_ownerships'])
top_ownerships.to_excel(ownerships_file)


cwd = os.path.abspath('') 
files = os.listdir(cwd) 


df2 = pd.DataFrame()
for file in files:
     if file.endswith('.xlsx'):
         df2 = df2.append(pd.read_excel(file), ignore_index=True) 

df2.head()

df2.to_excel(filename)