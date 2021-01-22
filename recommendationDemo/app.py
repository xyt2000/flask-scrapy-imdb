from flask import Flask
from flask import Flask, request, render_template,url_for, redirect
from datetime import timedelta
from dao.userDao import UserDao
from dao.recommendationdao import RecommendationDao
from dao.moviedao import MovieDao
from recommendationOfUser import getRecommendationByUser,getShowMovie,getRadom
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "FLASKTESTPROJECT"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # SESSION的超时时间

userName = ""
movieList = []
@app.route('/')
def hello_world():
    return render_template('login.html')



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
            if userCollect['collectid'] != '':
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
    print("movieid")
    print(id)
    userCollect = userDao.getcommendationByUsername(userName)
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
    return render_template('main.html', userName=userName, showList = showList)

@app.route('/main.html', methods=['GET', 'POST'])
def main():
    global userName
    userDao = UserDao()
    global movieList
    showList = []
    # 请求转发
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

if __name__ == '__main__':

    app.run()

