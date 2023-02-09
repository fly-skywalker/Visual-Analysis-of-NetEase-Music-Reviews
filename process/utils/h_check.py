import os
import pandas as pd
import json

data = pd.read_csv("../data/songid/songs.csv", encoding = "utf-8")


have_got = []

for root, _, files in os.walk("D:\BaiduNetdiskDownload\songs_comments"):
    for f in files:
        with open(os.path.join(root, f), 'r', encoding='utf-8') as fin:
            d = json.load(fin)
            have_got.append(d["songid"])

print(len(have_got))

not_yet = pd.DataFrame(columns = data.columns)

for _, r in data.iterrows():
    if r["songid"] not in have_got:
        print(r)
        not_yet.loc[len(not_yet), :] = r

print(not_yet)