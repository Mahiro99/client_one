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
asset = json.loads(response.text)

wb = Workbook()
defaultSheet = wb.active
defaultSheet.title = "assetData"

mylist = ['asset_contract', 'collection', 'traits', 'owner', 'creator', 'orders', 'top_ownerships', 'last_sale']
for sections in asset:
    if sections in mylist and isinstance(asset[sections], dict):
        sec = wb.create_sheet(sections)
        for key, value in asset[sections].items():
            print(key, '-->', value, "0")
            if isinstance(value, list):
                innerSec = wb.create_sheet(sections+"_"+key)
                for item in value:
                    for k, v in item.items():
                        print(k, '-->', v, "1")
                        innerSec.append([k, v])
            elif isinstance(value, dict):
                innerSec = wb.create_sheet(sections+"_"+key)
                for k, v in value.items():
                    if isinstance(v, dict):
                        for m, n in v.items():
                            if isinstance(n, dict):
                                for a,b in n.items():
                                    print(a, '-->', b, "21")
                                    innerSec.append([a, b])
                            else:
                                print(m, '-->', n, "21")
                                innerSec.append([m, n])
                    else:
                        print(k, '-->', v, "22")
                        innerSec.append([k, v])
            else:
                print(key, '-->', value)
                sec.append([key, str(value)])

    # for indexed data, might wanna save it excel in a diff format instead of key value
    elif sections in mylist and isinstance(asset[sections], list):
        sec = wb.create_sheet(sections)
        for item in asset[sections]:
            for k, v in item.items():
                print(k, '-->', v, "3")
                if isinstance(v, dict):
                    innerSec = wb.create_sheet(sections+ '_' + k)
                    for x, y in v.items():
                        print(x, '-->', y, "WOOO", type(y))
                        if isinstance(y, dict):
                            for m, n in y.items():
                                print(m, '-->', n, "5")
                                innerSec.append([m, n])
                        else:
                            print(x, '-->', y, "6")
                            innerSec.append([x, y])
                else:                
                    print(k, '-->', v, "4")
                    sec.append([k, v])
    else:
        print(type(asset[sections]))
        print(sections, '-->', asset[sections], "4")
        defaultSheet.append([sections, str(asset[sections])])


wb.save(filename="AssetObject.xlsx")
# [smth, smth, smth, smth, smth, smth
#     1, 2, 3, 4, 5, 6,
#     2, 3,4,5,6,7,8,
# ]