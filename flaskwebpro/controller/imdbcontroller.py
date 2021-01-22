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

@imdbcontroller.route("/getratecounts",methods=['GET', 'POST'])
def getRateCounts():
    imdbDao=ImdbDao()
    data=imdbDao.statisticRateCounts()
    ratecount={'8.0以下':0,'8.0-8.5':0,'8.5-9.0':0,'9.0以上':0}
    for k in data:
        if float(k['rating'])<8:
            ratecount['8.0以下']+=k['s']
        elif float(k['rating'])>=8.0 and float(k['rating'])<8.5:
            ratecount['8.0-8.5'] += k['s']
        elif float(k['rating'])>=8.5 and float(k['rating'])<=9.0:
            ratecount['8.5-9.0'] += k['s']
        elif float(k['rating'])>9.0:
            ratecount['9.0以上'] += k['s']
    ratelist=[]
    for b in ratecount:
        dic={'rating':'','s':''}
        dic['rating']=b
        dic['s']=ratecount[b]
        ratelist.append(dic)
    return jsonify(ratelist)
    pass

@imdbcontroller.route("/getmetascorecounts",methods=['GET', 'POST'])
def getMetaScore():
    imdbDao=ImdbDao()
    data=imdbDao.statisticMetaScoreCounts()
    metacount={'60以下':0,'60-70':0,'70-80':0,'80-90':0,'90以上':0,}
    for k in data:
        if k['metascore']==None:
            pass
        else:
            if int(k['metascore']) < 60:
                metacount['60以下'] += k['s']
            elif int(k['metascore']) >= 60 and int(k['metascore']) < 70:
                metacount['60-70'] += k['s']
            elif int(k['metascore']) >= 70 and int(k['metascore']) < 80:
                metacount['70-80'] += k['s']
            elif int(k['metascore']) >= 80 and int(k['metascore']) < 90:
                metacount['80-90'] += k['s']
            elif int(k['metascore']) > 90:
                metacount['90以上'] += k['s']
    metalist=[]
    for b in metacount:
        dic={'metascore':'','s':''}
        dic['metascore']=b
        dic['s']=metacount[b]
        metalist.append(dic)
    return jsonify(metalist)


@imdbcontroller.route("/getdurationcounts",methods=['GET', 'POST'])
def getDurationCounts():
    imdbDao = ImdbDao()
    data=imdbDao.statisticDurationCounts()
    durationcount={'90分钟以下':0,'90分钟-120分钟':0,'120分钟以上':0}
    for k in data:
        if len(k['duration'])==8 and k['duration'][1]=='h':
            hour = int(k['duration'][0])
            minute=int(k['duration'][3:5])
        elif len(k['duration'])==7 and k['duration'][1]=='h':
            hour = int(k['duration'][0])
            minute=int(k['duration'][3:4])
        elif  len(k['duration'])==2 and  k['duration'][1]=='h':
            hour = int(k['duration'][0])
            minute = 0
        elif len(k['duration'])<7 and   k['duration'][1]!='h':
            hour=0
            minute = int(k['duration'][0:2])

        totaltime=hour*60+minute;

        if totaltime<90:
            durationcount['90分钟以下'] +=k['s']
        elif totaltime>=90 and totaltime<=120:
            durationcount['90分钟-120分钟'] += k['s']
        elif totaltime>120:
            durationcount['120分钟以上'] += k['s']

    durationlist=[]
    for b in durationcount:
        dic = {'value': '', 'name': ''}
        dic['name'] = b
        dic['value'] = int(durationcount[b])
        durationlist.append(dic)
    return jsonify(durationlist)


@imdbcontroller.route("/gettop5gross",methods=['GET', 'POST'])
def getTop5gross():
    imdbDao = ImdbDao()
    data = imdbDao.statisticTop5()
    return jsonify(data);
