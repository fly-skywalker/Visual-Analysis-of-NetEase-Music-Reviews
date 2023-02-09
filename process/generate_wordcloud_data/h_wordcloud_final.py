import pandas as pd
import jieba
import jieba.analyse

import os
from tqdm import tqdm

import json

for root, _, files in os.walk("out/songdata"):
    for i in tqdm(range(len(files))):
        print(files[i])
        #if os.path.exists("tfidf/wc_" + files[i][:-4] + ".json"):
        #    print("file already existed")
        #    continue
        data = pd.read_csv(os.path.join(root, files[i]), encoding = "utf-8")
        res = []
        for j in range(10):
            d = data[data['label'] == j]
            if d.shape[0] == 0:
                break
            reviews = ""
            for _, r in d.iterrows():
                reviews += r["comment"]
            l = jieba.analyse.extract_tags(reviews, topK=31, withWeight = True)
            for item in l:
                if item[0] != "首歌":
                    res.append({"text": item[0], "size": item[1] / max([k[1] for k in l]), "label": j})
        with open('tfidf/wc_' + files[i][:-4] + '.json', 'w', encoding='utf-8') as fout:
            json.dump(res, fout, indent = 4, ensure_ascii = False)
        

