from flask import Blueprint, jsonify, request,render_template
from dao.moviedao import MovieDao
from dao.recommendationdao import RecommendationDao
import  jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
import nltk
import re

nltk.download('punkt')
movieDao = MovieDao()
recommendationDao = RecommendationDao()
movieList = movieDao.getMovies()
content = []
for movie in movieList:
    movieInfo = movie.get('recommendation').replace("\n", "")
    #str = re.sub('[^\w ]', '', movieInfo)
    movieInfo = ' '.join(jieba.cut(movieInfo))
    content.append(movieInfo)
    pass
print(content)
vectorizer = CountVectorizer()
# 传入词库，用于统计词库和词数
tf = vectorizer.fit_transform(content)
# 得到词库。词汇表
words = vectorizer.get_feature_names()
print(words)
# 查看词频统计
print(tf.toarray())  #
tfidfTransformer = TfidfTransformer()
# 计算tf-idf
tfidf = tfidfTransformer.fit_transform(tf)
# 查看每句话的tf-idf值
print(tfidf.toarray())
from sklearn.metrics.pairwise import linear_kernel

# 通过向量的余弦相似度，计算出第一个文本和所有其他文本之间的相似度（注意此处包含了自己）
for t in range(len(movieList)):
    print(t)
    current = movieList[t]
    cosine_similarities = linear_kernel(tfidf[t], tfidf).flatten()
    #print(cosine_similarities)
    returnList = []
    for i in range(13):
        index = np.argmax(cosine_similarities)
        returnList.append(movieList[index])
        cosine_similarities[index] = -1
    recommendIds = ""
    for j in returnList:
        if recommendIds == "":
            recommendIds = recommendIds  +  str(j.get('id'))
        else:
            recommendIds = recommendIds + '-' + str(j.get('id'))
    params = [str(current.get('id')), recommendIds]
    print(params)
    recommendationDao.insertRecommend(params)
    recommendationDao.commit()
    print("插入成功")

