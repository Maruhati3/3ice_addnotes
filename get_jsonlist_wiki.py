import requests
from bs4 import BeautifulSoup
import json
import os

bpmUrl = [
    "https://w.atwiki.jp/asigami/pages/436.html",
    "https://w.atwiki.jp/asigami/pages/19.html",
    "https://w.atwiki.jp/asigami/pages/18.html",
    "https://w.atwiki.jp/asigami/pages/17.html",
    "https://w.atwiki.jp/asigami/pages/15.html",
    "https://w.atwiki.jp/asigami/pages/14.html",
    "https://w.atwiki.jp/asigami/pages/13.html",
    "https://w.atwiki.jp/asigami/pages/234.html",
    "https://w.atwiki.jp/asigami/pages/335.html",
    "https://w.atwiki.jp/asigami/pages/558.html",
    "https://w.atwiki.jp/asigami/pages/1056.html",
    "https://w.atwiki.jp/asigami/pages/1418.html"
]

DATA_FILE = "data_ashigami.json"

diff_map = {
    "(習)": "bSP",
    "(楽)": "BSP",
    "(踊)": "DSP",
    "(激)": "ESP",
    "(鬼)": "CSP",
}


def valid(v):
    return str(v).strip() not in {"", "-", "－"}


# ==========================================
# 今回取得分
# ==========================================

music_dict = {}

for url in bpmUrl:

    print("reading", url)

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")


    #################################################
    # ここから
    #################################################

    tables = soup.find_all("table")

    best_table = None
    best_count = 0


    for table in tables:

        count = sum(
            len(tr.find_all("td")) == 4
            for tr in table.find_all("tr")
        )


        if count > best_count:
            best_count = count
            best_table = table


    print("best_count:", best_count)


    if best_table is None:
        continue


    #################################################
    # ここまで
    #################################################


    for tr in best_table.find_all("tr"):

        tds = tr.find_all("td")

        if len(tds) != 4:
            continue


        title_diff = tds[0].get_text(strip=True)

        ver = tds[1].get_text(strip=True)
        bpm = tds[2].get_text(strip=True)
        value = tds[3].get_text(strip=True)



        diff = None


        for suffix,key in diff_map.items():

            if title_diff.endswith(suffix):

                title = title_diff[:-len(suffix)].strip()

                diff = key

                break


        if diff is None:
            continue



        if title not in music_dict:

            music_dict[title]={

                "title":title,

                "BPM":"",
                "ver":"",

                "bSP":"",
                "BSP":"",
                "DSP":"",
                "ESP":"",
                "CSP":"",

                "BDP":"",
                "DDP":"",
                "EDP":"",
                "CDP":"",

            }


        music=music_dict[title]


        if valid(bpm):
            music["BPM"]=bpm


        if valid(ver):
            music["ver"]=ver


        if valid(value):
            music[diff]=value



print("fetched:",len(music_dict))


for tr in best_table.find_all("tr"):

    tds = tr.find_all("td")

    if len(tds) != 4:
        continue


    title_diff = tds[0].get_text(strip=True)
    ver = tds[1].get_text(strip=True)
    bpm = tds[2].get_text(strip=True)
    value = tds[3].get_text(strip=True)


    diff = None
    title = None


    for suffix, key in diff_map.items():

        if title_diff.endswith(suffix):

            title = title_diff[:-len(suffix)].strip()
            diff = key
            break


    if diff is None:
        continue


    if title not in music_dict:

        music_dict[title] = {

            "title": title,

            "BPM": "",
            "ver": "",

            "bSP": "",
            "BSP": "",
            "DSP": "",
            "ESP": "",
            "CSP": "",

            "BDP": "",
            "DDP": "",
            "EDP": "",
            "CDP": "",
        }


    music = music_dict[title]


    if valid(bpm):
        music["BPM"] = bpm


    if valid(ver):
        music["ver"] = ver


    if valid(value):
        music[diff] = value

print("fetched:", len(music_dict))



# ==========================================
# data.json 読み込み
# ==========================================

if os.path.exists(DATA_FILE):

    with open(DATA_FILE, encoding="utf-8") as f:
        old_data = json.load(f)

else:

    old_data = []


saved_dict = {
    m["title"]: m
    for m in old_data
}



# ==========================================
# マージ
# ==========================================

added = 0
updated = 0


for title, music in music_dict.items():


    if title not in saved_dict:

        saved_dict[title] = music
        added += 1
        continue


    old = saved_dict[title]


    for key in music.keys():

        if key == "title":
            continue


        old_val = old.get(key, "")
        new_val = music[key]


        if valid(new_val) and old_val != new_val:

            old[key] = new_val
            updated += 1



# ==========================================
# 保存
# ==========================================

merged = list(saved_dict.values())


with open(DATA_FILE, "w", encoding="utf-8") as f:

    json.dump(
        merged,
        f,
        ensure_ascii=False,
        indent=2
    )


print()
print(f"追加曲数 : {added}")
print(f"更新項目数 : {updated}")
print(f"総曲数 : {len(merged)}")