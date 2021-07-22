import requests
import json
import pandas as pd
from openpyxl import Workbook
import os

asset_contract_address = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"
token_id = 1
fetchSingleAsset = 'https://api.opensea.io/api/v1/asset/{}/{}'.format(
    asset_contract_address, token_id)

response = requests.request("GET", fetchSingleAsset)
asset = json.loads(response.text)

wb = Workbook()
defaultSheet = wb.active
defaultSheet.title = "assetData"
mylist = ['asset_contract', 'collection', 'traits', 'owner',
          'creator', 'orders', 'top_ownerships', 'last_sale']

def getAllDataFromAssetAndConverToExcelSheets():
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
                                    for a, b in n.items():
                                        print(a, '-->', b, "2")
                                        innerSec.append([a, b])
                                else:
                                    print(m, '-->', n, "3")
                                    innerSec.append([m, n])
                        else:
                            print(k, '-->', v, "4")
                            innerSec.append([k, v])
                else:
                    print(key, '-->', value, 5)
                    sec.append([key, str(value)])

        # for indexed data, might wanna save it excel in a diff format instead of key value
        elif sections in mylist and isinstance(asset[sections], list):
            sec = wb.create_sheet(sections)
            for item in asset[sections]:
                for k, v in item.items():
                    print(k, '-->', v, "6")
                    if isinstance(v, dict):
                        innerSec = wb.create_sheet(sections + '_' + k)
                        for x, y in v.items():
                            print(x, '-->', y, "WOOO", "7")
                            if isinstance(y, dict):
                                for m, n in y.items():
                                    print(m, '-->', n, "8")
                                    innerSec.append([m, n])
                            else:
                                print(x, '-->', y, "9")
                                innerSec.append([x, y])
                    else:
                        print(k, '-->', v, "10")
                        sec.append([k, v])
        else:
            print(sections, '-->', asset[sections], "11")
            defaultSheet.append([sections, str(asset[sections])])
    wb.save(filename="AssetObject.xlsx")

# getAllDataFromAssetAndConverToExcelSheets()
