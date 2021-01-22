import random

from dao.recommendationdao import RecommendationDao
from dao.moviedao import MovieDao
def getRecommendationByUser(collect):
    recommendationDao = RecommendationDao()
    movieDao = MovieDao()
    recommendList = []
    collectMovie = collect['collectid'].split('-')
    for movieId in collectMovie:
        recommendMovieIds = (recommendationDao.getRecommendationByMovieId(str(movieId)))['recommendId'].split('-')
        for recommendMovieId in recommendMovieIds:
            recommenMovie =  movieDao.getMovieById(recommendMovieId)
            recommendList.append(recommenMovie)
    return recommendList

def getShowMovie(MovieList,num):
    showList = []
    if num == 1:
        return MovieList
    else:
        i = 0
        j = 0
        m = 0
        while i <12:
            m = i + 1
            showList.append(MovieList[j])
            if m % num == 0:
                j = (j+13+1)%(13*num)
            else:
                j = j + 13
            i = i + 1
        return showList

def getRadom(movieList):
    showList = []
    res = random.sample(range(0, len(movieList)), 12)
    for r in res:
        showList.append(movieList[r])
    return showList

