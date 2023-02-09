import os
import pickle

from gensim.models import word2vec

vs = 300
mc = 100
name = 'model_' + str(vs) + '_' + str(mc)


from tqdm import tqdm
for root, _, files in os.walk("processed_reviews"):
    #for i in tqdm(range(len(files))): #61458
    processed_reviews = []
    for i in tqdm(range(0, 12291)):
        list_file = open(os.path.join(root, files[i]), "rb")
        review = pickle.load(list_file)
        list_file.close()
        processed_reviews += review
    model = word2vec.Word2Vec(processed_reviews, workers = 8, vector_size = vs, min_count = mc, window = 5, sample = 1e-3)
    print('语料数：', model.corpus_count)
    print('词表长度：', len(model.wv.index_to_key))

    processed_reviews = []
    for i in tqdm(range(12291, 24582)):
        list_file = open(os.path.join(root, files[i]), "rb")
        review = pickle.load(list_file)
        list_file.close()
        processed_reviews += review
    model.build_vocab(processed_reviews, update = True)
    model.train(processed_reviews, total_examples = model.corpus_count, epochs = model.epochs)
    print('语料数：', model.corpus_count)
    print('词表长度：', len(model.wv.index_to_key))

    processed_reviews = []
    for i in tqdm(range(24582, 36873)):
        list_file = open(os.path.join(root, files[i]), "rb")
        review = pickle.load(list_file)
        list_file.close()
        processed_reviews += review
    model.build_vocab(processed_reviews, update = True)
    model.train(processed_reviews, total_examples = model.corpus_count, epochs = model.epochs)
    print('语料数：', model.corpus_count)
    print('词表长度：', len(model.wv.index_to_key))

    processed_reviews = []
    for i in tqdm(range(36873, 49164)):
        list_file = open(os.path.join(root, files[i]), "rb")
        review = pickle.load(list_file)
        list_file.close()
        processed_reviews += review
    model.build_vocab(processed_reviews, update = True)
    model.train(processed_reviews, total_examples = model.corpus_count, epochs = model.epochs)
    print('语料数：', model.corpus_count)
    print('词表长度：', len(model.wv.index_to_key))

    processed_reviews = []
    for i in tqdm(range(49164, 61458)):
        list_file = open(os.path.join(root, files[i]), "rb")
        review = pickle.load(list_file)
        list_file.close()
        processed_reviews += review
    model.build_vocab(processed_reviews, update = True)
    model.train(processed_reviews, total_examples = model.corpus_count, epochs = model.epochs)
    print('语料数：', model.corpus_count)
    print('词表长度：', len(model.wv.index_to_key))


    model.init_sims(replace = True)
    model.save(name) 


