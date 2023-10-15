from bs4 import BeautifulSoup
import requests
import json
import time

while True:
    url = "https://coinmarketcap.com/"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")

    tbody = soup.tbody
    trs = tbody.contents
    data = {}
    for tr in trs[0:2]:
        name = tr.contents[2].p.string
        price = tr.contents[3].span.string
        symbol = tr.find(class_="coin-item-symbol").string
        data[name] = {"symbol": symbol, "price": price}

    # Mở tệp JSON và cập nhật dữ liệu
    with open("coin_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Update Data!!!")
    time.sleep(15)
