import requests
import json
import pandas as pd

url = "https://api.opensea.io/api/v1/asset/0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5/5477"

response = requests.request("GET", url)
final_dictionary = json.loads(response.text)
print(final_dictionary['traits'])

df = pd.DataFrame.from_dict(final_dictionary, orient='index')
df = df.transpose()
df.to_excel('file1.xlsx')

