from flask import Flask, request, render_template,url_for, redirect
from datetime import timedelta
from dao.userdao import UserDao
from controller.datacontroller import datacontroller
from controller.jobcontroller import jobcontroller
from controller.imdbcontroller import imdbcontroller
from dao.imdbdao import ImdbDao
from dao.recommendationdao import RecommendationDao
from dao.moviedao import MovieDao
from recommendationOfUser import getRecommendationByUser,getShowMovie,getRadom

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "FLASKTESTPROJECT"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # SESSION的超时时间
app.register_blueprint(datacontroller)
app.register_blueprint(jobcontroller)
app.register_blueprint(imdbcontroller)

userName = ""
movieList = []








@app.route("/")
def index1():
    return render_template("login.html")

@app.route('/index1.html',methods=['GET', 'POST'])
def index():
    imdbDao=ImdbDao()
    paramDict={}
    if request.method == "POST":
        searhName = request.form.get('searchName')
        pageSize = request.form.get('pageSize')
        currentPage = request.form.get('currentPage')
        paramDict['searchName'] = searhName
        if pageSize==None and currentPage==None:
            paramDict['pageSize'] = pageSize
            paramDict['currentPage'] = currentPage
        else:
            paramDict['pageSize'] = int(pageSize)
            paramDict['currentPage'] = int(currentPage)
    else:
        pass
    if paramDict.get('pageSize') == None or paramDict.get('currentPage') == None:
        paramDict['pageSize'] = 10
        paramDict['currentPage'] = 1
        pass
    if not paramDict.get('searchName'):
        paramDict['searchName'] = ""
        pass
    showList = imdbDao.getImdbPage(paramDict)
    counts = imdbDao.getImdbCounts(paramDict).get("counts")
    # 计算总共有多少页
    totalPage = int(counts // paramDict.get('pageSize')) if counts % paramDict.get('pageSize') == 0 else int(counts // paramDict.get('pageSize'))+1

    paramDict['totalPage'] = totalPage
    paramDict['counts'] = counts
    return render_template('index1.html',showList=showList, paramDict=paramDict)

@app.route('/main.html', methods=['GET', 'POST'])
def main():
    global userName
    userDao = UserDao()
    global movieList
    showList = []
    # 请求推荐数据
    userCollect = userDao.getcommendationByUsername(userName)
    if userCollect['collectid'] != '':
        movies = userCollect['collectid'].split('-')
        movieList = getRecommendationByUser(userCollect)
        num = len(movies)
        showList = getShowMovie(movieList, num)
        return render_template('main.html', name=userName, showList=showList)
    else:
        return render_template('main.html', name=userName, showList=showList)

@app.route('/collect.html', methods=['GET', 'POST'])
def collect():
    global userName
    userDao = UserDao()
    collectList = []
    movieDao = MovieDao()
    print(userName)
    userCollect = userDao.getcommendationByUsername(userName)
    print(userCollect)
    collectMovie = userCollect['collectid'].split('-')
    for MovieId in collectMovie:
        recommenMovie = movieDao.getMovieById(MovieId)
        collectList.append(recommenMovie)
    return render_template('collect.html',userName = userName,movieList = collectList)
@app.route('/matplotlib.html', methods=['GET', 'POST'])
def matplotlib():
    return render_template('matplotlib.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    userDao = UserDao()
    paramDict = {}
    if  request.method == "POST":
        opr = request.form.get('opr')
        if opr == "add":
            userName = request.form.get('userName')
            phoneno = request.form.get('phoneno')
            email = request.form.get('email')
            params = [userName, '123456', '', 0, phoneno, email]
            result = userDao.createUser(params)
            userDao.commit()
        elif opr == "update":
            id =  request.form.get('id')
            phoneno = request.form.get('phoneno')
            email = request.form.get('email')
            params = [phoneno, email]
            result = userDao.updateUser(params, id)
            userDao.commit()
            pass
        elif opr == "search":
            searhName = request.form.get('searchName')
            pageSize = request.form.get('pageSize')
            currentPage = request.form.get('currentPage')
            paramDict['searchName'] = searhName
            paramDict['pageSize'] = int(pageSize)
            paramDict['currentPage'] = int(currentPage)
            pass
    else:
        opr = request.args.get("opr")
        if opr == "disable":
            id = request.args.get('id')
            userDao.disableUserByUserId(id)
            userDao.commit()
            pass
        pass
    if paramDict.get('pageSize') == None or paramDict.get('currentPage') == None:
        paramDict['pageSize'] = 10
        paramDict['currentPage'] = 1
        pass

    if not paramDict.get('searchName'):
        paramDict['searchName'] = ""
        pass
    userList = userDao.getUserListPage(paramDict)
    counts = userDao.getUserCounts(paramDict).get("counts")
    # 计算总共有多少页
    totalPage = int(counts // paramDict.get('pageSize')) if counts % paramDict.get('pageSize') == 0 else int(counts // paramDict.get('pageSize'))+1

    paramDict['totalPage'] = totalPage
    paramDict['counts'] = counts
    return render_template('sys/user.html', userList=userList, paramDict=paramDict)

@app.route("/about/<name>")
def about(name):
    return name + "你好啊"
    pass

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        global userName
        userDao = UserDao()
        userName = request.form['userName']
        userPwd  = request.form['userPwd']
        user = userDao.getUserByUserName(userName)
        print(userName)
        print(userPwd)
        print(user)
        global  movieList
        showList = []
        if user and user.get('password') == userPwd:
            # 请求转发
            userCollect = userDao.getcommendationByUsername(userName)
            print(userCollect)
            if userCollect['collectid'] != None:
                movies= userCollect['collectid'].split('-')
                movieList = getRecommendationByUser(userCollect)
                num = len(movies)
                showList = getShowMovie(movieList,num)
                return render_template('main.html', name=userName,showList = showList )
            else:
                return render_template('main.html', name=userName, showList=showList)
        else:
            return "登录失败"
        pass
    else:
        return render_template('login.html', msg='登录失败')
    pass

@app.route('/change', methods=['GET', 'POST'])
def change():
    global movieList
    showList = getRadom(movieList)
    return render_template('main.html', name=userName,showList = showList )

@app.route('/collect', methods=['GET', 'POST'])
def collectMovie():
    global userName
    userDao = UserDao()
    id = request.args.get('id')
    userCollect = userDao.getcommendationByUsername(userName)
    if userCollect['collectid'] != None:
        collectMovie = userCollect['collectid'].split('-')
        print(collectMovie)
        newCollect = userCollect['collectid']
        if str(id) not in collectMovie:
            newCollect = userCollect['collectid'] + '-' + str(id)
        userDao.setCollect(userName,newCollect)
        userCollect = userDao.getcommendationByUsername(userName)
        movieList = getRecommendationByUser(userCollect)
        num = len(userCollect)
        showList = getShowMovie(movieList, num)
    else:
        userDao.setCollect(userName, str(id))
        userCollect = userDao.getcommendationByUsername(userName)
        movieList = getRecommendationByUser(userCollect)
        num = len(userCollect)
        showList = getShowMovie(movieList, num)
    return render_template('main.html', userName=userName, showList = showList)

if __name__ == '__main__':
    app.run()
