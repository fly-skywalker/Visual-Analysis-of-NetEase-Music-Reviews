import pandas as pd
import jieba
import jieba.analyse

import os
from tqdm import tqdm

import json

songs_info = pd.read_csv("songid/songs.csv")
songids = songs_info["songid"].tolist()
singerids = songs_info["artistid"].tolist()

for root, _, files in os.walk("songdata"):
    for i in tqdm(range(len(files))):
#         print(files[i])
        #if os.path.exists("tfidf/wc_" + files[i][:-4] + ".json"):
        #    print("file already existed")
        #    continue

#         _id = int(files[i][:-4])
#         idx = -1
#         songname = ""
#         singername = ""
#         try:
#             idx = songids.index(_id)
#             songname = songs_info.loc[idx, "song"]
#             singername = songs_info.loc[idx, "artist"]
#         except ValueError:
#             try:
#                 idx = singerids.index(_id)
#                 singername = songs_info.loc[idx, "artist"]
#             except ValueError:
#                 pass
#
# #         print(idx)
# #         print(songname)
# #         print(singername)

        data = pd.read_csv(os.path.join(root, files[i]), encoding = "utf-8")
        res = []
        max_size = 0
        for j in range(10):
            d = data[data['label'] == j]
            if d.shape[0] == 0:
                break
            reviews = ""
            for _, r in d.iterrows():
                reviews += r["comment"]
            l = jieba.analyse.extract_tags(reviews, topK=31, withWeight = True)
            try:
#                 max_size = max(max_size, max([k[1] for k in l]))
                max_size = max([k[1] for k in l])
            except ValueError:
                continue
            for item in l:
                if item[0] != "首歌":
#                 if item[0] != "首歌" and item[0] != singername and item[0] != songname:
#                     max_size = max([k[1] for k in l])
#                     res.append({"text": item[0], "size": item[1] / max([k[1] for k in l]), "label": j})
                    res.append({"text": item[0], "size": item[1] / max_size, "label": j})

#         for i, item in enumerate(res):
#             res[i]['size'] /= max_size

        with open('tfidf/wc_' + files[i][:-4] + '.json', 'w', encoding='utf-8') as fout:
            json.dump(res, fout, indent = 4, ensure_ascii = False)
        

