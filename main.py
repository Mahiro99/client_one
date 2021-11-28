#!/usr/bin/env python
import requests
import json
import pandas as pd
import time
# asset_contract_address = "0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5"

def getTheMainStuff(asset_contract_address, tokenList, timeInterval):
    output = pd.DataFrame()
    myTraits = {}
    for id in tokenList:
        for x in range(id[0], id[1]):
            print('-->', x, 'Completed')
            fetchSingleAsset = 'https://api.opensea.io/api/v1/asset/{}/{}'.format(
                asset_contract_address, x)
            
            time.sleep(timeInterval)
            response = requests.request("GET", fetchSingleAsset)
            final_dictionary = json.loads(response.text)

            makeBool = True
            for key, value in final_dictionary.items():
                if key == 'last_sale' and value is None:
                    makeBool = False
                    break
            
            if final_dictionary['owner']['user'] == None:
                tempDict = {"username": "null"}
                final_dictionary['owner']['user'] = tempDict
            
            if final_dictionary['creator'] == None:
                tempDict = {"user": {"username": "null"}}
                final_dictionary['creator'] = tempDict
                
            if final_dictionary['creator']['user'] == None:
                tempDict = {"username": "null"}
                final_dictionary['creator']['user'] = tempDict
            
            current_price = calculateETHprice(final_dictionary)

            if makeBool:
                generalInfo = {
                    'Collection Name': final_dictionary['collection']['primary_asset_contracts'][0]['name'],
                    'Project Contract Address': final_dictionary['collection']['primary_asset_contracts'][0]['address'],
                    'External Link ': final_dictionary['collection']['primary_asset_contracts'][0]['external_link'],
                    'Created Date': final_dictionary['collection']['primary_asset_contracts'][0]['created_date'],
                    'Schema Name': final_dictionary['collection']['primary_asset_contracts'][0]['schema_name'],
                    'Symbol': final_dictionary['collection']['primary_asset_contracts'][0]['symbol'],
                    'Creator User': final_dictionary['creator']['user']['username'],
                    'NFT Name': final_dictionary['name'],
                    'Token ID': final_dictionary['token_id'],
                    'Auction Type': final_dictionary['last_sale']['auction_type'],
                    'Total Price': final_dictionary['last_sale']['total_price'],
                    'Last Sale Creation Date': final_dictionary['last_sale']['created_date'],
                    'Quantity': final_dictionary['last_sale']['quantity'],
                    'Telegram URL': final_dictionary['collection']['telegram_url'],
                    'Twitter User': final_dictionary['collection']['twitter_username'],
                    'Instagram User': final_dictionary['collection']['instagram_username'],
                    'Discord URL': final_dictionary['collection']['discord_url'],
                    # ETH Price
                    'Current Price': current_price,
                    'Permalink': final_dictionary['permalink'],
                    'Total NFTs in Collection': final_dictionary['collection']['stats']['total_supply'],
                    'Owner': final_dictionary['owner']['user']['username'],
                }
            else:
                generalInfo = {
                    'Collection Name': final_dictionary['collection']['primary_asset_contracts'][0]['name'],
                    'Project Contract Address': final_dictionary['collection']['primary_asset_contracts'][0]['address'],
                    'External Link ': final_dictionary['collection']['primary_asset_contracts'][0]['external_link'],
                    'Created Date': final_dictionary['collection']['primary_asset_contracts'][0]['created_date'],
                    'Schema Name': final_dictionary['collection']['primary_asset_contracts'][0]['schema_name'],
                    'Symbol': final_dictionary['collection']['primary_asset_contracts'][0]['symbol'],
                    'Creator User': final_dictionary['creator']['user']['username'],
                    'NFT Name': final_dictionary['name'],
                    'Token ID': final_dictionary['token_id'],
                    'Auction Type': final_dictionary['last_sale'],
                    'Total Price': final_dictionary['last_sale'],
                    'Last Sale Creation Date': final_dictionary['last_sale'],
                    'Quantity': final_dictionary['last_sale'],
                    'Telegram URL': final_dictionary['collection']['telegram_url'],
                    'Twitter User': final_dictionary['collection']['twitter_username'],
                    'Instagram User': final_dictionary['collection']['instagram_username'],
                    'Discord URL': final_dictionary['collection']['discord_url'],
                    'Current Price': current_price,  # ETH Price
                    'Permalink': final_dictionary['permalink'],
                    'Total NFTs in Collection': final_dictionary['collection']['stats']['total_supply'],
                    'Owner': final_dictionary['owner']['user']['username'],
                }


            mytraits = getTokenStuff(final_dictionary)
            for trait_type, valAndCountList in mytraits.items():
                if len(valAndCountList[0]) == 3:
                    generalInfo['Traits: ' + trait_type] = valAndCountList[0][0]
                    generalInfo['Traits: ' + trait_type + ' (#) '] = valAndCountList[0][1]
                    generalInfo['Traits: ' + trait_type + ' (%) ']  = (valAndCountList[0][2] / final_dictionary['collection']['stats']['total_supply']) * 100 
                else:
                    generalInfo['Traits: ' + trait_type] = valAndCountList[0][0]
                    generalInfo['Traits: ' + trait_type + ' (#) '] = valAndCountList[0][1]
                    generalInfo['Traits: ' + trait_type + ' (%) ']  = (valAndCountList[0][1] / final_dictionary['collection']['stats']['total_supply']) * 100 

            output = output.append(generalInfo, ignore_index=True)
        output = getScore(output)
    return output

def getScore(output):
    df2 = output.filter(regex='#')
    list1 = []
    scoreList= []
    maxMinList = []
    sums= []
    for index, row in df2.iterrows():
        for key, value in df2.items():
            print(value, "VALUE")
            if type(df2[key].iloc[index]) == str:
                continue
            else:
                x = float(df2[key].iloc[index])
                list1.append(x)
            max = float(df2[key].max())
            min = float(df2[key].min())
            maxMinList.append([max, min])
        list1 = [0 if pd.isna(x) else x for x in list1]
        print(list1, "value list")
        for x in list1:
            if x!=0:
                diff = maxMinList[0][0]-maxMinList[0][1]
                if diff == 0:
                    scores = 1
                else:
                    scores = 1 + (x - maxMinList[0][1])*4/(diff)
                scoreList.append(scores)
                del maxMinList[0]
                print(x, '-->', maxMinList, "MaxMinList")
        sums.append(sum(scoreList))
        list1.clear()
        scoreList.clear()
        maxMinList.clear()
  
    output['Rarity Sniper Score'] = sums
    return output

def getTokenStuff(final_dictionary):
    traits = final_dictionary['traits']
    myTraits = {}
    mylist = []
    count = 0
    for type in traits:
        for key, value in type.items():
            if key == 'trait_type':
                mylist = [val for val in type.values() if val !=
                          value and val != None ]
                if value in myTraits:
                    count +=1
                    myTraits[value+str(count)] = mylist
                else:
                    myTraits[value] = mylist
                
    normalizedTraits = pd.json_normalize(myTraits)
    return normalizedTraits


def getSummaryStuff(asset_contract_address, token):
    output = pd.DataFrame()
    fetchSingleAsset = 'https://api.opensea.io/api/v1/asset/{}/{}'.format(
        asset_contract_address, token)
    response = requests.request("GET", fetchSingleAsset)
    final_dictionary = json.loads(response.text)

    name = final_dictionary['asset_contract']['name']
    total_supply = final_dictionary['collection']['stats']['total_supply']
    total_owners = final_dictionary['collection']['stats']['num_owners']
    floor_price = final_dictionary['collection']['stats']['floor_price']
    total_volume_traded = final_dictionary['collection']['stats']['total_volume']
    description = final_dictionary['asset_contract']['description']
    summaryInfo = {
        "Name": name,
        "Total Items": total_supply,
        "Total Owners": total_owners,
        "Floor Price": floor_price,
        "Total Volume Traded": total_volume_traded,
        "Description": description,
    }
    output = output.append(summaryInfo, ignore_index=True)
    return output


def calculateETHprice(final_dictionary):
    price = 0
    eth_price_calc = 1000000000000000000
    if len(final_dictionary['orders']) == 0 or len(final_dictionary['auctions']) != 0:
        for item in final_dictionary['auctions']:
            for key, value in item.items():
                if key == 'current_price':
                    price = float(value) / eth_price_calc
        final_dictionary['orders'] = 'None'
        
    else:
        last_current_price = len(final_dictionary['orders']) - 1
        for key,value in final_dictionary['orders'][last_current_price].items():
            if key == 'current_price':
                price = float(value) / eth_price_calc
    return price

def startScrape():
    asset_contract_address = str(input("Enter Contract Address: "))
    numOfRanges = int(input("Choose number of ranges: "))
    final_list = [[int(input("Enter a number and press enter(Every 2 numbers will be a range): ")) for _ in range(2)] for _ in range(numOfRanges)]
    timeInterval = float(input("Interval between each token(ms). Standard is 0.4: "))

    writer = pd.ExcelWriter('Final.xlsx')

    df = getTheMainStuff(asset_contract_address, final_list, timeInterval)
    summaryDf = getSummaryStuff(asset_contract_address, 1)

    df.to_excel(writer, sheet_name='General Info', index=True)
    summaryDf.to_excel(writer, sheet_name='Summary', index=True)
    writer.save()
    input("Press enter to exit")

startScrape()
