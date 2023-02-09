###########################################################################################
### h_process_comments.py BY hyh                                                        ###
### README:                                                                             ###
### 读取w2v模型，将评论转换为向量                                                         ###
###########################################################################################
import numpy as np
import opencc
import re
import jieba
cc = opencc.OpenCC('t2s')
from gensim.models import Word2Vec


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

import threading

def thread_process_sentence(model, sentence_words, sentence_feature, word_count, bow, stopwords, thread_id, thread_count):
    for i in range(thread_id, len(sentence_words), thread_count):
        for word in sentence_words[i]:
            if word not in stopwords and word in bow: #remove stopwords
                word_count[thread_id] += 1
                sentence_feature[thread_id] += model.wv[word]

def w2v_mt(model_path, stopwords_path, review):
    model = Word2Vec.load(model_path)

    stopwords = []
    if stopwords_path != None:
        
        with open(stopwords_path, 'r', encoding = "utf-8") as stop:
            stopwords = stop.read().splitlines()

    thread_count = 8

    sentence_words = review2words(review)
    word_count = [0] * thread_count
    sentence_feature = []
    for i in range(thread_count):
        sentence_feature.append(np.zeros(int(model_path.split('_')[1]))) #vector dim
    bow = model.wv.index_to_key

    threads = []
    for i in range(thread_count):
        threads.append(threading.Thread(target = thread_process_sentence, args = (model, sentence_words, sentence_feature, word_count, bow, stopwords, i, thread_count)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    total_word_count = sum(word_count)
    if total_word_count < 5: #remove short comments
        return None
    total_sentence_feature = np.zeros(int(model_path.split('_')[1]))
    for i in range(thread_count):
        total_sentence_feature += sentence_feature[i]

    total_sentence_feature /= total_word_count

    return total_sentence_feature

def w2v(model_path, stopwords_path, review):
    model = Word2Vec.load(model_path)

    stopwords = []
    if stopwords_path != None:
        
        with open(stopwords_path, 'r', encoding = "utf-8") as stop:
            stopwords = stop.read().splitlines()

    sentence_words = review2words(review)
    word_count = 0
    sentence_feature = np.zeros(int(model_path.split('_')[1])) #vector dim
    bow = model.wv.index_to_key

    for sentence in sentence_words:
        for word in sentence:
            if word not in stopwords and word in bow: #remove stopwords
                word_count += 1
                sentence_feature += model.wv[word]
    if word_count < 5: #remove short comments
        return None
    sentence_feature /= word_count

    return sentence_feature


### DEBUG ###
#print(w2v("model300", "stopwords", '有一種開心 是活在當下 回憶過去 暢想未來 有一種憂傷亦是如此。能留下任何存留的痕跡都是一種奇蹟。proudly proclaim that my life so far is a 小奇蹟. 献给世界第1好的自己，加我qq， 1234567889'))