###########################################################################################
### h_final_train.py BY hyh                                                             ###
### README:                                                                             ###
### 读取 **所有** 评论json文件，训练w2v模型                                               ###
### 可以调整的参数：1、匹配原则（如数字、英语、表情等处理方案）                              ###
###                2、w2v算法、vectorsize、min_count、window等参数        ！              ###
###########################################################################################

import os
import json

from tqdm import tqdm

import opencc
import re
import jieba

jieba.initialize ()

from gensim.models import word2vec

cc = opencc.OpenCC('t2s')

def review2words(review):
    sentences = re.split('[^\u4e00-\u9fa5a-zA-Z0-9]', cc.convert(review.strip())) 
    #繁转简，删除前后空格；按非汉字、英语、数字分句
    seperated_sen = []
    for sen in sentences:
        sen = re.sub('[^\u4e00-\u9fa5]', '', sen) #删除汉字以外的字符
        #optional: 保留英文，但是空格检测困难，且英文训练样本较少，故去除
        if len(sen) == 0: #移除长度为0的句子
            continue
        words = jieba.lcut(sen) #jieba分词
        seperated_sen.append(words)

    return seperated_sen

#例句
#print(review2words('有一種開心 是活在當下 回憶過去 暢想未來 有一種憂傷亦是如此。能留下任何存留的痕跡都是一種奇蹟。proudly proclaim that my life so far is a 小奇蹟. 献给世界第1好的自己，加我qq， 1234567889'))

ONLY_TRAIN = False
processed_reviews = []

import pickle

if not ONLY_TRAIN:
    for root, _, files in os.walk("D:\BaiduNetdiskDownload\songs_comments"):
    #for root, _, files in os.walk("songs_comments"):
        for i in tqdm(range(len(files))):
            f = files[i]
            print(f)
            with open(os.path.join(root, f), 'r', encoding='utf-8') as fin:
                data = json.load(fin)
                id = data['songid']
                for i in data['hot_comments']:
                    try:
                        res = review2words(i['content'])
                    except:
                        pass
                    processed_reviews += res
                for i in data['comments']:
                    try:
                        res = review2words(i['content'])
                    except:
                        pass
                    processed_reviews += res
            list_file = open("processed_reviews/" + str(id) + ".pickle", "wb")
            pickle.dump(processed_reviews, list_file)
            list_file.close()
            processed_reviews = []
            ### DEBUG ###
            #break
            ### DEBUG ###

    print(len(processed_reviews))

    


else:

    list_file = open("processed_reviews.pickle", "rb")
    processed_reviews = pickle.load(list_file)
    list_file.close()
'''
vs = 300
mc = 100

#default: CBOW
model = word2vec.Word2Vec(processed_reviews, workers = 8, vector_size = vs, min_count = mc, window = 5, sample = 1e-3)
model.init_sims(replace = True)

model.save('model_' + str(vs) + '_' + str(mc))
'''

