import requests
from bs4 import BeautifulSoup
import json

url = "https://bemaniwiki.com/?DanceDanceRevolution+WORLD/%C1%B4%B6%CA%C1%ED%A5%CE%A1%BC%A5%C4%BF%F4%A5%EA%A5%B9%A5%C8"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

keys = [
    "title", 
    "bSP", "BSP", "DSP", "ESP", "CSP",
    "BDP", "DDP", "EDP", "CDP",
]

result = []

for tr in soup.find_all("tr"):
    tds = tr.find_all("td")
    if len(tds) == 10:
        values = [td.get_text(" ", strip=True) for td in tds]
        result.append(dict(zip(keys, values)))

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
