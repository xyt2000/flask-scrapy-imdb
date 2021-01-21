from flask import Flask, request, render_template,url_for, redirect
from datetime import timedelta
from dao.userdao import UserDao
from controller.datacontroller import datacontroller
from controller.jobcontroller import jobcontroller
from controller.imdbcontroller import imdbcontroller
from dao.imdbdao import ImdbDao

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "FLASKTESTPROJECT"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # SESSION的超时时间
app.register_blueprint(datacontroller)
app.register_blueprint(jobcontroller)
app.register_blueprint(imdbcontroller)

@app.route('/index',methods=['GET', 'POST'])
def index():
    imdbDao=ImdbDao()
    paramDict={}

    if paramDict.get('pageSize') == None or paramDict.get('currentPage') == None:
        paramDict['pageSize'] = 10
        paramDict['currentPage'] = 1
        pass

    if not paramDict.get('searchName'):
        paramDict['searchName'] = ""
        pass

    searhName = request.form.get('searchName')
    pageSize = request.form.get('pageSize')
    currentPage = request.form.get('currentPage')
    paramDict['searchName'] = searhName
    paramDict['pageSize'] = int(pageSize)
    paramDict['currentPage'] = int(currentPage)

    imdbList = imdbDao.getImdbPage(paramDict)
    counts = imdbDao.getImdbCounts(paramDict).get("counts")
    # 计算总共有多少页
    totalPage = int(counts // paramDict.get('pageSize')) if counts % paramDict.get('pageSize') == 0 else int(counts // paramDict.get('pageSize'))+1

    paramDict['totalPage'] = totalPage
    paramDict['counts'] = counts
    return render_template('index1.html',imdbList=imdbList, paramDict=paramDict)




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
        userDao = UserDao()
        userName = request.form['userName']
        userPwd  = request.form['userPwd']
        user = userDao.getUserByUserName(userName)
        if user and user.get('password') == userPwd:
            # 请求转发
            return render_template('dashboard.html', name=userName)
        else:
            return "登录失败"
        pass
    else:
        return render_template('login.html', msg='登录失败')
    pass

if __name__ == '__main__':
    app.run()
