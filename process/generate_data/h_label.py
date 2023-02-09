from h_process_comments import w2v

import numpy as np
import pandas as pd

import json

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as MSE
import matplotlib.pyplot as plt
import seaborn as sns

import math

from tqdm import tqdm
import os

import jieba
jieba.initialize ()


model = "model_300_100"


for root, _, files in os.walk("D:\BaiduNetdiskDownload\songs_comments"):
    for i in tqdm(range(len(files))):
        f = files[i]

        original_comments = []
        comments = []
        timestamp = []
        liked = []
        ishot = []

        fid = -1
        catid = -1
        artistid = -1

        data = None

        with open(os.path.join(root, f), 'r', encoding='utf-8') as fin:
            data = json.load(fin)
            fid = data['songid']
            catid = data['catid']
            artistid = data['artistid']

        path = "out/songdata/" + str(fid) + ".csv"
        print(path)

        if os.path.exists(path) or catid != 1001:
            continue

        with open(os.path.join(root, f), 'r', encoding='utf-8') as fin:

            for i in data['hot_comments']:
                vec = w2v(model, None, i['content'])
                if vec is None:
                    continue
                original_comments.append([i['content']])
                comments.append(vec)
                timestamp.append([i['t']])
                liked.append([i['likedCount']])
                ishot.append([1])
            for i in data['comments']:
                vec = w2v(model, None, i['content'])
                if vec is None:
                    continue
                original_comments.append([i['content']])
                comments.append(vec)
                timestamp.append([i['t']])
                liked.append([i['likedCount']])
                ishot.append([0])

        test_df = pd.DataFrame(data = comments)

        ### PCA ###
        pca = PCA(n_components = 2)
        try:
            pca.fit(test_df)
        except:
            continue
        data_pca = pca.transform(test_df)
        df_pca = pd.DataFrame(data = data_pca, columns = ['first', 'second'])

        ### KMeans ###
        SSE = []
        final_k = 8

        skip = False
        for k in range(1, 11):
            kms = KMeans(n_clusters = k)
            try:
                kms.fit(test_df)
                SSE.append(kms.inertia_)
            except:
                skip = True
                final_k = k - 1
                break
            


        if skip != True:
            max_angle = -99999999

            for k in range(2, 10):
                reg1 = LinearRegression()
                reg1.fit([[i] for i in range(1, k + 1)], SSE[0 : k])
                a1 = reg1.coef_[0]

                reg2 = LinearRegression()
                reg2.fit([[i] for i in range(k, 11)], SSE[k - 1 :])
                a2 = reg2.coef_[0]  

                #print(k, abs(math.atan2(a2, 1) - math.atan2(a1, 1)))
                if abs(math.atan2(a2, 1) - math.atan2(a1, 1)) > max_angle:
                    max_angle = abs(math.atan2(a2, 1) - math.atan2(a1, 1))
                    final_k = k


        kmeans = KMeans(n_clusters = final_k)

        kmeans.fit(test_df)

        df_pca_kms = pd.concat([df_pca, pd.DataFrame(data = [[i] for i in kmeans.labels_], columns = ['label'])], axis = 1)

        ### DRAW ###
        '''
        from color import my_color
        usecolor = my_color[0 : final_k]
        usecolor.insert(0, usecolor[-1])
        usecolor = usecolor[0 : final_k]

        sns.scatterplot(data = df_pca_kms, x = 'first', y = 'second', hue = 'label', palette = sns.color_palette(usecolor))
        plt.show()
        '''

        ### SAVE ###
        test_all = pd.concat([pd.DataFrame(data = original_comments, columns = ['comment']), pd.DataFrame(data = timestamp, columns = ['time']), pd.DataFrame(data = liked, columns = ['likes']), pd.DataFrame(data = ishot, columns = ['ishot']), df_pca_kms], axis = 1)

        #test_all.to_csv("out/songdata/" + str(fid) + '.csv', index = False)
        test_all.to_csv("out/songdata/" + str(fid) + '.csv', index = False)

