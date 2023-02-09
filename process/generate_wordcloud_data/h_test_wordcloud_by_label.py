import numpy as np
import pandas as pd
import opencc
import re
import jieba
cc = opencc.OpenCC('t2s')
from gensim.models import Word2Vec

from wordcloud import WordCloud
from wordcloud import get_single_color_func

def review2words_for_wc(review, stopwords_path):
    stopwords = []
    with open(stopwords_path, 'r', encoding = "utf-8") as stop:
        stopwords = stop.read().splitlines()
    sentences = re.split('[^\u4e00-\u9fa5a-zA-Z0-9]', cc.convert(review.strip())) 
    #繁转简，删除前后空格；按非汉字、英语、数字分句
    seperated_sen = []
    for sen in sentences:
        #sen = re.sub('[^\u4e00-\u9fa5]', '', sen) #删除汉字以外的字符
        #optional: 保留英文，但是空格检测困难，且英文训练样本较少，故去除
        if len(sen) == 0: #移除长度为0的句子
            continue
        words_raw = jieba.lcut(sen) #jieba分词
        words = []
        for w in words_raw:
            if w not in stopwords:
                words.append(w.strip())
        seperated_sen.append("/".join(words))

    return "/".join(seperated_sen)


df = pd.read_csv('data/label_test.csv')

types = 0
for i in range(10):
    if df[df['label'] == i].shape[0] == 0:
        types = i
        break


from color import my_color
usecolor = my_color[0 : types]
usecolor.insert(0, usecolor[-1])
usecolor = usecolor[0 : types]


for i in range(10):
    reviews = []
    data = df[df['label'] == i]
    if data.shape[0] == 0:
        break
    
    reviews = []
    for _, r in data.iterrows():
        reviews.append(review2words_for_wc(r['comment'], "stopwords.txt"))
    wordcloud = WordCloud(font_path = 'simfang.ttf', color_func = get_single_color_func(usecolor[r['label']]), background_color = "white").generate("/".join(reviews))
    wordcloud.to_file('../data/test_label' + str(i) + '.jpg')

