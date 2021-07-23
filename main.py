import requests
import json
import pandas as pd
from openpyxl import Workbook
import os
 
asset_contract_address = "0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5"
token_id = 5477
fetchSingleAsset = 'https://api.opensea.io/api/v1/asset/{}/{}'.format(
    asset_contract_address, token_id)

response = requests.request("GET", fetchSingleAsset)
final_dictionary = json.loads(response.text)

for x in final_dictionary.values():
    if x is None:
       x = str('None')



generalInfo = {'Name': final_dictionary['collection']['primary_asset_contracts'][0]['name'],'Address':final_dictionary['collection']['primary_asset_contracts'][0]['address'],
'Description':final_dictionary['collection']['primary_asset_contracts'][0]['description'], 'External Link ': final_dictionary['collection']['primary_asset_contracts'][0]['external_link'],
'Created Date': final_dictionary['collection']['primary_asset_contracts'][0]['created_date'], 'Schema Name': final_dictionary['collection']['primary_asset_contracts'][0]['schema_name'],
'Symbol': final_dictionary['collection']['primary_asset_contracts'][0]['symbol'], 'Payout Address': final_dictionary['collection']['primary_asset_contracts'][0]['payout_address'],
'Creator User': final_dictionary['creator']['user']['username'], 'NFT Name':final_dictionary['asset_contract']['name'], 'Token ID':final_dictionary['token_id'],
'Owner': final_dictionary['owner']['user']['username'], 'Permalink': final_dictionary['permalink']}

otherInfo = {'Event Type ':final_dictionary['last_sale']['event_type'], 'Event Timestamp': final_dictionary['last_sale']['event_timestamp'],
'Auction Type': final_dictionary['last_sale']['auction_type'], 'Total Price': final_dictionary['last_sale']['total_price'],
'Last Sale Creation Date': final_dictionary['last_sale']['created_date'], 'Quantity': final_dictionary['last_sale']['quantity'],
'Telegram URL':final_dictionary['collection']['telegram_url'], 'Twitter User': final_dictionary['collection']['twitter_username'],
'Instagram User': final_dictionary['collection']['instagram_username'], 'Wiki URL': final_dictionary['collection']['wiki_url'],
'Discord URL': final_dictionary['collection']['discord_url'], 'ETH Price': final_dictionary['last_sale']['payment_token']['eth_price'],
'USD Price': final_dictionary['last_sale']['payment_token']['usd_price'], 'Address of Last Transaction': final_dictionary['last_sale']['transaction']['from_account']['address']}



traits = pd.json_normalize(final_dictionary['traits'])

df_1 = pd.DataFrame(generalInfo, index=[0])
df_2 = pd.DataFrame(traits)
df_3 = pd.DataFrame(otherInfo, index=[0])

writer = pd.ExcelWriter('Final.xlsx')

df_1.to_excel(writer, sheet_name = 'General Info', index=True)
df_2.to_excel(writer, sheet_name = 'Traits', index = False)
df_3.to_excel(writer, sheet_name = 'Other Info', index = False)


writer.save()



# def getAllDataFromAssetAndConverToExcelSheets():
#     wb = Workbook()
#     defaultSheet = wb.active
#     defaultSheet.title = "assetData"
#     mylist = ['asset_contract', 'collection', 'traits', 'owner',
#             'creator', 'orders', 'top_ownerships', 'last_sale']

#     for sections in asset:
#         if sections in mylist and isinstance(asset[sections], dict):
#             sec = wb.create_sheet(sections)
#             for key, value in asset[sections].items():
#                 print(key, '-->', value, "0")
#                 if isinstance(value, list):
#                     innerSec = wb.create_sheet(sections+"_"+key)
#                     for item in value:
#                         for k, v in item.items():
#                             print(k, '-->', v, "1")
#                             innerSec.append([k, v])
#                 elif isinstance(value, dict):
#                     innerSec = wb.create_sheet(sections+"_"+key)
#                     for k, v in value.items():
#                         if isinstance(v, dict):
#                             for m, n in v.items():
#                                 if isinstance(n, dict):
#                                     for a, b in n.items():
#                                         print(a, '-->', b, "2")
#                                         innerSec.append([a, b])
#                                 else:
#                                     print(m, '-->', n, "3")
#                                     innerSec.append([m, n])
#                         else:
#                             print(k, '-->', v, "4")
#                             innerSec.append([k, v])
#                 else:
#                     print(key, '-->', value, 5)
#                     sec.append([key, str(value)])

#         # for indexed data, might wanna save it excel in a diff format instead of key value
#         elif sections in mylist and isinstance(asset[sections], list):
#             sec = wb.create_sheet(sections)
#             for item in asset[sections]:
#                 for k, v in item.items():
#                     print(k, '-->', v, "6")
#                     if isinstance(v, dict):
#                         innerSec = wb.create_sheet(sections + '_' + k)
#                         for x, y in v.items():
#                             print(x, '-->', y, "WOOO", "7")
#                             if isinstance(y, dict):
#                                 for m, n in y.items():
#                                     print(m, '-->', n, "8")
#                                     innerSec.append([m, n])
#                             else:
#                                 print(x, '-->', y, "9")
#                                 innerSec.append([x, y])
#                     else:
#                         print(k, '-->', v, "10")
#                         sec.append([k, v])
#         else:
#             print(sections, '-->', asset[sections], "11")
#             defaultSheet.append([sections, str(asset[sections])])
#     wb.save(filename="AssetObject.xlsx")

# # getAllDataFromAssetAndConverToExcelSheets()
