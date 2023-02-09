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

import threading

thread_num = 8


def read_comments_mt(data, model, original_comments, comments, timestamp, liked, ishot, thread_id, thread_num):
    for i in range(thread_id, len(data["comments"]), thread_num):
        vec = w2v(model, None, data["comments"][i]['content'])
        if vec is None:
            continue
        original_comments[thread_id].append([data["comments"][i]['content']])
        comments[thread_id].append(vec)
        timestamp[thread_id].append([data["comments"][i]['t']])
        liked[thread_id].append([data["comments"][i]['likedCount']])
        ishot[thread_id].append([0])


model = "model_300_100"

for root, _, files in os.walk("D:\BaiduNetdiskDownload\songs_comments"):
    for i in tqdm(range(len(files))):
        f = files[i]

        original_comments = []
        comments = []
        timestamp = []
        liked = []
        ishot = []
        for j in range(thread_num):
            original_comments.append([])
            comments.append([])
            timestamp.append([])
            liked.append([])
            ishot.append([])
        total_original_comments = []
        total_comments = []
        total_timestamp = []
        total_liked = []
        total_ishot = []

        fid = -1
        catid = -1

        data = None

        with open(os.path.join(root, f), 'r', encoding='utf-8') as fin:
            data = json.load(fin)
            fid = data['songid']
            catid = data['catid']

        path = "out/songdatatest/" + str(fid) + ".csv"
        print(path)

        if os.path.exists(path):
            continue

        with open(os.path.join(root, f), 'r', encoding='utf-8') as fin:

            for j in data['hot_comments']:
                vec = w2v(model, None, j['content'])
                if vec is None:
                    continue
                total_original_comments.append([j['content']])
                total_comments.append(vec)
                total_timestamp.append([j['t']])
                total_liked.append([j['likedCount']])
                total_ishot.append([1])
            threads = []
            for j in range(thread_num):
                threads.append(threading.Thread(target = read_comments_mt, args = (data, model, original_comments, comments, timestamp, liked, ishot, j, thread_num)))
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            for j in range(thread_num):
                total_original_comments += original_comments[j]
                total_comments += comments[j]
                total_timestamp += timestamp[j]
                total_liked += liked[j]
                total_ishot += ishot[j]

        

        test_df = pd.DataFrame(data = total_comments)

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

        min_k = 4
        max_k = 8


        skip = False
        for k in range(min_k - 1, max_k + 1):
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

            for k in range(min_k, max_k):
                reg1 = LinearRegression()
                reg1.fit([[i] for i in range(min_k - 1, k + 1)], SSE[0 : k])
                a1 = reg1.coef_[0]

                reg2 = LinearRegression()
                reg2.fit([[i] for i in range(k, max_k + 1)], SSE[k - 1 :])
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
        test_all = pd.concat([pd.DataFrame(data = total_original_comments, columns = ['comment']), pd.DataFrame(data = total_timestamp, columns = ['time']), pd.DataFrame(data = total_liked, columns = ['likes']), pd.DataFrame(data = total_ishot, columns = ['total_ishot']), df_pca_kms], axis = 1)

        #test_all.to_csv("out/songdata/" + str(fid) + '.csv', index = False)
        test_all.to_csv("out/songdatatest/" + str(fid) + '.csv', index = False)

