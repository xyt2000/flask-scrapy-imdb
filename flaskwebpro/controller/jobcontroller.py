from flask import Blueprint, jsonify, request,render_template
from dao.jobdao import JobDao
import  jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

jobcontroller = Blueprint('jobcontroller', __name__)

@jobcontroller.route("/jobview",methods=['GET',"POST"])
def jobview():
    jobDao = JobDao()

    profile = request.form.get("introduction")

    jobList = jobDao.getJobList()

    # 就是要编写基于内容的推荐功能
    content = []
    profile = ' '.join(jieba.cut(profile))
    content.append(profile)
    for job in jobList:
        jobText = job.get('jobdetail')
        jobText = ' '.join(jieba.cut(jobText))
        content.append(jobText)
        pass

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
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    print(cosine_similarities)
    cosine_similarities = cosine_similarities[1:]

    returnList = []
    # 取前10条
    for i in range(10):
        index = np.argmax(cosine_similarities)
        returnList.append(jobList[index])
        cosine_similarities[index] = -1
        pass
    return render_template('dashboard.html', returnList=returnList)
    pass