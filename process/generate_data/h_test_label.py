from h_process_comments import w2v

# print(w2v("model300", "stopwords", '有一種開心 是活在當下 回憶過去 暢想未來 有一種憂傷亦是如此。能留下任何存留的痕跡都是一種奇蹟。proudly proclaim that my life so far is a 小奇蹟. 献给世界第1好的自己，加我qq， 1234567889'))

import numpy as np
import pandas as pd

import json

test_file = "../data/songs_comments/孤勇者_1901371647.json"

original_comments = []
comments = []
timestamp = []
liked = []
ishot = []

with open(test_file, 'r', encoding='utf-8') as fin:
    data = json.load(fin)
    for i in data['hot_comments']:
        vec = w2v("model_test", None, i['content'])
        if vec is None:
            continue
        original_comments.append([i['content']])
        comments.append(vec)
        timestamp.append([i['t']])
        liked.append([i['likedCount']])
        ishot.append([1])
    for i in data['comments']:
        vec = w2v("model_test", None, i['content'])
        if vec is None:
            continue
        original_comments.append([i['content']])
        comments.append(vec)
        timestamp.append([i['t']])
        liked.append([i['likedCount']])
        ishot.append([0])

test_df = pd.DataFrame(data=comments)

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as MSE

import matplotlib.pyplot as plt
import seaborn as sns

### PCA ###
pca = PCA(n_components=2)

pca.fit(test_df)
data_pca = pca.transform(test_df)
df_pca = pd.DataFrame(data=data_pca, columns=['first', 'second'])

### KMeans ###
SSE = []
final_k = 8
for k in range(1, 11):
    kms = KMeans(n_clusters=k)
    kms.fit(test_df)
    SSE.append(kms.inertia_)

# min_mse = 99999999
max_angle = -99999999

import math

for k in range(2, 10):
    reg1 = LinearRegression()
    reg1.fit([[i] for i in range(1, k + 1)], SSE[0: k])
    # pred1 = reg1.predict([[i] for i in range(1, k + 1)])
    # mse1 = MSE(pred1, SSE[0 : k])
    a1 = reg1.coef_[0]

    reg2 = LinearRegression()
    reg2.fit([[i] for i in range(k, 11)], SSE[k - 1:])
    # pred2 = reg2.predict([[i] for i in range(k, 11)])
    # mse2 = MSE(pred2, SSE[k - 1 :])
    a2 = reg2.coef_[0]

    # if mse1 + mse2 < min_mse:
    #    final_k = k
    #    min_mse = mse1 + mse2
    print(k, abs(math.atan2(a2, 1) - math.atan2(a1, 1)))
    if abs(math.atan2(a2, 1) - math.atan2(a1, 1)) > max_angle:
        max_angle = abs(math.atan2(a2, 1) - math.atan2(a1, 1))
        final_k = k

kmeans = KMeans(n_clusters=final_k)

kmeans.fit(test_df)

df_pca_kms = pd.concat([df_pca, pd.DataFrame(data=[[i] for i in kmeans.labels_], columns=['label'])], axis=1)

### DRAW ###
# from matplotlib.colors import ListedColormap

from color import my_color

usecolor = my_color[0: final_k]
usecolor.insert(0, usecolor[-1])
usecolor = usecolor[0: final_k]

# sns.scatterplot(data = df_pca_kms, x = 'first', y = 'second', hue = 'label', palette = "Accent")

sns.scatterplot(data=df_pca_kms, x='first', y='second', hue='label', palette=sns.color_palette(usecolor))
plt.show()

### SAVE ###
test_all = pd.concat(
    [pd.DataFrame(data=original_comments, columns=['comment']), pd.DataFrame(data=timestamp, columns=['time']),
     pd.DataFrame(data=liked, columns=['likes']), pd.DataFrame(data=ishot, columns=['ishot']), df_pca_kms], axis=1)

test_all.to_csv("../data/label_test.csv", index=False)
