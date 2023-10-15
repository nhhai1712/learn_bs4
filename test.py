from bs4 import BeautifulSoup
import requests
import json

url = "https://coinmarketcap.com/" 
response = requests.get(url).text
soup = BeautifulSoup(response, "html.parser")

tbody = soup.tbody
trs = tbody.contents
data = {}
for tr in trs:
    name = tr.contents[2].p.string
    price = tr.contents[3].span.string
    symbol = tr.find(class_="coin-item-symbol").string
    data[name] = {"symbol": symbol, "price": price}

# print(data)
with open("coin_data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

