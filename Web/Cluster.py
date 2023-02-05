import codecs
import json

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
import jieba
import numpy as np
from sklearn.externals import joblib

INPUT_FILE = "WithRank.json"
STOP_WORD_FILE = "stopword.txt"
OUT_PUT_FILE = "WithCluster.json"
WORD_SET_PATH = "wordset.txt"


def Read_Data(input_file):
    f = open(input_file, 'r', encoding='UTF-8')
    data = []
    for line in f.readlines():
        data.append(eval(line.strip())['RecruitPostName'][0])
    return data


def stop_words_read(input_file):
    fp = open(input_file, 'r', encoding='UTF-8')
    words = fp.read()
    result = jieba.cut(words)
    new_words = []
    for r in result:
        new_words.append(r)
    return set(new_words)


def del_stop_word(words, stop_words):
    res_mat = []
    for w in words:
        new_words = []
        result = jieba.cut(w)
        for r in result:
            if r not in stop_words:
                new_words.append(r)
        res_mat.append(new_words)
    return res_mat


def get_VEC(matrs, word_set, stop_word):
    new_words = []
    result = jieba.cut(matrs)
    for r in result:
        if r not in stop_word:
            new_words.append(r)
    res = []
    for w in word_set:
        res.append(new_words.count(w) * 1.0)
    return np.array(res)


def get_vector(matrs):
    word_set = set()
    docs = []
    for m in matrs:
        docs.append(m)
        word_set |= set(m)
    word_set = list(word_set)
    f = codecs.open(filename=WORD_SET_PATH, mode='wb', encoding='utf-8')
    for w in word_set:
        f.write(w + '\n')
    f.close()
    docs_vsm = []

    for doc in docs:
        tmp_vec = []
        for word in word_set:
            tmp_vec.append(doc.count(word) * 1.0)

        docs_vsm.append(tmp_vec)

    docs_matrix = np.array(docs_vsm)
    return word_set, docs_matrix


def get_TF_IDF(matrix):
    tf_idf_transformer = TfidfTransformer()
    tf_idf = tf_idf_transformer.fit_transform([matrix])
    x_train_weight = tf_idf.toarray()
    return x_train_weight


def KMeans_Cluster(Weight, clusters):
    my_kms = KMeans(n_clusters=clusters)
    y = my_kms.fit_predict(Weight)
    joblib.dump(my_kms, "model.pkl")
    return y


def store_cluster(res):
    f = open(INPUT_FILE, 'r', encoding='UTF-8')
    file = codecs.open(filename=OUT_PUT_FILE, mode='wb', encoding='utf-8')
    i = 0
    for line in f.readlines():
        cur_j = eval(line.strip())
        cur_j["Cluster"] = str(res[i])
        text = json.dumps(cur_j, ensure_ascii=False) + "\n"
        file.write(text)
        i += 1
    file.close()
    f.close()


def predict(X):
    my_kms = joblib.load("./model.pkl")
    stop_word = stop_words_read(STOP_WORD_FILE)
    result = []
    fp = open(WORD_SET_PATH, 'r', encoding='UTF-8')
    for line in fp.readlines():
        result.append(line.strip())
    print(len(result))
    VEC = get_VEC(X, stop_word=stop_word, word_set=result)
    weight = get_TF_IDF(VEC)
    return my_kms.predict(weight)[0]


if __name__ == '__main__':
    # source = Read_Data(INPUT_FILE)
    # stop_word = stop_words_read(STOP_WORD_FILE)
    # mats = del_stop_word(source, stop_word)
    # word_set, VEC = get_vector(mats)
    # weight = get_TF_IDF(VEC)
    # res = KMeans_Cluster(weight, 7)
    # res = np.array(res)
    # store_cluster(res)
    text = "微信经理"
    print(predict(text))
