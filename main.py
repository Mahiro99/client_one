import requests
import json
import pandas as pd
from openpyxl import Workbook
import os
import time


eth_price_calc = 1000000000000000000
asset_contract_address = "0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5"
token_idList = [7656,
                7117,
                2696,
                6209,
                6903,
                7085,
                9341,
                1591,
                9752,
                8699,
                5755,
                3828,
                8986,
                5344,
                5682,
                9755,
                4823,
                1735,
                5868,
                4815,
                5637,
                5860,
                9641,
                822,
                8495,
                695,
                4876,
                5956,
                8925,
                6286,
                6432,
                4416,
                1660,
                7583,
                565,
                9106,
                3523,
                8260,
                3032,
                2518,
                9762,
                36,
                3579,
                395,
                3379,
                9668,
                8217,
                1340,
                1314,
                1502,
                7412]


def getTheMainStuff():
    output = pd.DataFrame()
    for token in token_idList:
        print(token)
        fetchSingleAsset = 'https://api.opensea.io/api/v1/asset/{}/{}'.format(
            asset_contract_address, token)

        time.sleep(1)
        response = requests.request("GET", fetchSingleAsset)
        final_dictionary = json.loads(response.text)

        # doing this in a hacky way right now,
        makeBool = True
        for key, value in final_dictionary.items():
            if key == 'last_sale' and value is None:
                makeBool = False
                break
        
        anotherBool = True
        for key,value in final_dictionary.items():
            if key == 'orders' and value is None:
                anotherBool = False
                break

        # print(final_dictionary.keys(), "testing request time out for throttle")
        traits = pd.json_normalize(final_dictionary['traits'])
        Hat_value = ''
        Hat_trait_count = ''
        Background_value = ''
        Background_trait_count = ''
        Skin_value = ''
        Skin_trait_count = ''
        Clothes_value = ''
        Clothes_trait_count = ''
        Eyes_value = ''
        Eyes_trait_count = ''
        Mouth_value = ''
        Mouth_trait_count = ''

        for index, row in traits.iterrows():
            if row['trait_type'] == 'Hat':
                Hat_value = row['value']
                Hat_trait_count = row['trait_count']
            elif row['trait_type'] == 'Background':
                Background_value = row['value']
                Background_trait_count = row['trait_count']
            elif row['trait_type'] == 'Skin':
                Skin_value = row['value']
                Skin_trait_count = row['trait_count']
            elif row['trait_type'] == 'Clothes':
                Clothes_value = row['value']
                Clothes_trait_count = row['trait_count']
            elif row['trait_type'] == 'Eyes':
                Eyes_value = row['value']
                Eyes_trait_count = row['trait_count']
            elif row['trait_type'] == 'Mouth':
                Mouth_value = row['value']
                Mouth_trait_count = row['trait_count']

        if makeBool:
            # but i dont think usually youre supposed to hardcore values like that
            generalInfo = {'Collection Name': final_dictionary['collection']['primary_asset_contracts'][0]['name'], 'Address': final_dictionary['collection']['primary_asset_contracts'][0]['address'],
                           'External Link ': final_dictionary['collection']['primary_asset_contracts'][0]['external_link'],
                           'Created Date': final_dictionary['collection']['primary_asset_contracts'][0]['created_date'], 'Schema Name': final_dictionary['collection']['primary_asset_contracts'][0]['schema_name'],
                           'Symbol': final_dictionary['collection']['primary_asset_contracts'][0]['symbol'], 
                           'Creator User': final_dictionary['creator']['user']['username'], 'NFT Name': final_dictionary['name'], 'Token ID': final_dictionary['token_id'],
                           'Auction Type': final_dictionary['last_sale']['auction_type'], 'Total Price': final_dictionary['last_sale']['total_price'],
                           'Last Sale Creation Date': final_dictionary['last_sale']['created_date'], 'Quantity': final_dictionary['last_sale']['quantity'],
                           'Telegram URL': final_dictionary['collection']['telegram_url'], 'Twitter User': final_dictionary['collection']['twitter_username'],
                           'Instagram User': final_dictionary['collection']['instagram_username'], 'Wiki URL': final_dictionary['collection']['wiki_url'],
                           'Discord URL': final_dictionary['collection']['discord_url'], 'Current Price': float(final_dictionary['orders'][0]['current_price']) / eth_price_calc,
                            'Address of Last Transaction': final_dictionary['last_sale']['transaction']['from_account']['address'],
                           'Traits: Hat (#)': Hat_value + " ({}) ".format(Hat_trait_count),
                           'Traits: Skin (#)': Skin_value + " ({}) ".format(Skin_trait_count),
                           'Traits: Eyes (#)': Eyes_value + " ({}) ".format(Eyes_trait_count),
                           'Traits: Mouth (#)': Mouth_value + " ({}) ".format(Mouth_trait_count),
                           'Traits: Clothes (#)': Clothes_value + " ({}) ".format(Clothes_trait_count),
                           'Traits: Background (#)': Background_value + " ({}) ".format(Background_trait_count),
                           }
        elif makeBool == False or anotherBool == False:
            generalInfo = {'Collection Name': final_dictionary['collection']['primary_asset_contracts'][0]['name'], 'Address': final_dictionary['collection']['primary_asset_contracts'][0]['address'],
                            'External Link ': final_dictionary['collection']['primary_asset_contracts'][0]['external_link'],
                           'Created Date': final_dictionary['collection']['primary_asset_contracts'][0]['created_date'], 'Schema Name': final_dictionary['collection']['primary_asset_contracts'][0]['schema_name'],
                           'Symbol': final_dictionary['collection']['primary_asset_contracts'][0]['symbol'], 
                           'Creator User': final_dictionary['creator']['user']['username'], 'NFT Name': final_dictionary['name'], 'Token ID': final_dictionary['token_id'],
                           'Auction Type': final_dictionary['last_sale'], 'Total Price': final_dictionary['last_sale'],
                           'Last Sale Creation Date': final_dictionary['last_sale'], 'Quantity': final_dictionary['last_sale'],
                           'Telegram URL': final_dictionary['collection']['telegram_url'], 'Twitter User': final_dictionary['collection']['twitter_username'],
                           'Instagram User': final_dictionary['collection']['instagram_username'],
                           'Discord URL': final_dictionary['collection']['discord_url'], 'Current Price': final_dictionary['orders'],
                            'Address of Last Transaction': final_dictionary['last_sale'],
                           'Traits: Hat (#)': Hat_value + " ({}) ".format(Hat_trait_count),
                           'Traits: Skin (#)': Skin_value + " ({}) ".format(Skin_trait_count),
                           'Traits: Eyes (#)': Eyes_value + " ({}) ".format(Eyes_trait_count),
                           'Traits: Mouth (#)': Mouth_value + " ({}) ".format(Mouth_trait_count),
                           'Traits: Clothes (#)': Clothes_value + " ({}) ".format(Clothes_trait_count),
                           'Traits: Background (#)': Background_value + " ({}) ".format(Background_trait_count),
                           }
        output = output.append(generalInfo, ignore_index=True)
    return output


writer = pd.ExcelWriter('Final.xlsx')
df = getTheMainStuff()
df.to_excel(writer, sheet_name='General Info', index=True)
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
