import requests
from bs4 import BeautifulSoup
import json
import os

notesUrl = "https://bemaniwiki.com/?DanceDanceRevolution+WORLD/%C1%B4%B6%CA%C1%ED%A5%CE%A1%BC%A5%C4%BF%F4%A5%EA%A5%B9%A5%C8"
bpmUrl = "https://bemaniwiki.com/?DanceDanceRevolution+WORLD/%E5%85%A8%E6%9B%B2%E3%82%B3%E3%82%A2BPM%E3%83%AA%E3%82%B9%E3%83%88"

note_keys = [
    "title",
    "bSP", "BSP", "DSP", "ESP", "CSP",
    "BDP", "DDP", "EDP", "CDP",
]

DATA_FILE = "data.json"


def valid(v):
    return str(v).strip() not in {"", "-", "－"}


# -------------------------------
# ノーツ取得
# -------------------------------
response = requests.get(notesUrl)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

new_data = []

for tr in soup.find_all("tr"):
    tds = tr.find_all("td")

    if len(tds) == 10:
        values = [td.get_text(" ", strip=True) for td in tds]

        music = dict(zip(note_keys, values))

        # BPMを後から追加するため初期化
        music["display_bpm"] = ""
        music["core_bpm"] = ""

        new_data.append(music)


# -------------------------------
# BPM取得
# -------------------------------
response = requests.get(bpmUrl)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

bpm_dict = {}

for tr in soup.find_all("tr"):
    tds = tr.find_all("td")

    if len(tds) == 4:
        values = [td.get_text(" ", strip=True) for td in tds]

        title = values[0]

        bpm_dict[title] = {
            "display_bpm": values[1],
            "core_bpm": values[2]
        }


# -------------------------------
# BPM付与
# -------------------------------
for music in new_data:

    bpm = bpm_dict.get(music["title"])

    if bpm:
        music["display_bpm"] = bpm["display_bpm"]
        music["core_bpm"] = bpm["core_bpm"]


# -------------------------------
# 既存データ読み込み
# -------------------------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, encoding="utf-8") as f:
        old_data = json.load(f)
else:
    old_data = []


music_dict = {m["title"]: m for m in old_data}


# -------------------------------
# マージ
# -------------------------------
added = 0
updated = 0

for music in new_data:

    title = music["title"]

    if title not in music_dict:
        music_dict[title] = music
        added += 1
        continue

    old = music_dict[title]

    for key in music.keys():

        if key == "title":
            continue

        old_val = old.get(key, "")
        new_val = music.get(key, "")

        if valid(new_val) and old_val != new_val:
            old[key] = new_val
            updated += 1


# -------------------------------
# 保存
# -------------------------------
merged = list(music_dict.values())

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)


print(f"追加曲数 : {added}")
print(f"更新項目数 : {updated}")
print(f"総曲数   : {len(merged)}")