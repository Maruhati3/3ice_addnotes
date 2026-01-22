import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime as dt
url = "https://bemaniwiki.com/?DanceDanceRevolution+WORLD/%C1%B4%B6%CA%C1%ED%A5%CE%A1%BC%A5%C4%BF%F4%A5%EA%A5%B9%A5%C8"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

rows = []

for tr in soup.find_all("tr"):
    tds = tr.find_all("td")
    if len(tds) == 10:
        row = [td.get_text(strip=True) for td in tds]
        rows.append(row)

with open("output.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
