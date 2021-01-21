from flask import Blueprint, jsonify, request
from dao.imdbdao import ImdbDao

imdbcontroller=Blueprint('imdbcontroller',__name__)

@imdbcontroller.route("/getgenrecounts",methods=['GET', 'POST'])
def getGenreCounts():
    imdbDao=ImdbDao()
    data=imdbDao.statisticGenresCounts()
    return jsonify(data)
    pass

@imdbcontroller.route("/getyearcounts",methods=['GET', 'POST'])
def getYearCounts():
    imdbDao=ImdbDao()
    data=imdbDao.statisticYearCounts()
    yearcount={'2000年以后':0,'1950年之前':0,'1950-2000':0}
    for k in data:
        if int(k['release_date'])//1000==2:
            yearcount['2000年以后']+=k['s']
        elif int(k['release_date'])//1000==1 and (int(k['release_date'])//10)%10<=5:
            yearcount['1950年之前']+=k['s']
        elif int(k['release_date'])//1000==1 and (int(k['release_date'])//10)%10>5:
            yearcount['1950-2000'] += k['s']
    yearlist=[]
    for b in yearcount:
        dic={'value':'','name':''}
        dic['value']=int(yearcount[b])
        dic['name']=b
        yearlist.append(dic)
    return jsonify(yearlist)
    pass
