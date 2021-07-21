import requests
import json

url = "https://api.opensea.io/api/v1/asset/0x3fe1a4c1481c8351e91b64d5c398b159de07cbc5/5477"

response = requests.request("GET", url)
final_dictionary = json.loads(response.text)
print(final_dictionary["traits"])