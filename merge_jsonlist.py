import json


SRC_FILE = "data.json"
ASHI_FILE = "data_ashigami.json"
OUT_FILE = "merged.json"


def valid(v):
    return str(v).strip() not in {"", "-", "－"}


with open(SRC_FILE, encoding="utf-8") as f:
    src = json.load(f)

with open(ASHI_FILE, encoding="utf-8") as f:
    ashi = json.load(f)


src_dict = {
    m["title"]: m
    for m in src
}


merged = []

updated = 0


for music in ashi:

    title = music["title"]

    src_music = src_dict.get(title)

    if src_music is None:
        merged.append(music)
        continue


    new_music = music.copy()


    for key in [
        "bSP","BSP","DSP","ESP","CSP",
        "BDP","DDP","EDP","CDP"
    ]:

        old_val = new_music.get(key, "")
        src_val = src_music.get(key, "")


        if not valid(old_val) and valid(src_val):
            new_music[key] = src_val
            updated += 1


    merged.append(new_music)


with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        merged,
        f,
        ensure_ascii=False,
        indent=2
    )


print(f"補完項目数 : {updated}")
print(f"総曲数 : {len(merged)}")
print(f"保存先 : {OUT_FILE}")