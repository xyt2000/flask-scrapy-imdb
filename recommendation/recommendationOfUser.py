from dao.recommendationdao import RecommendationDao
from dao.moviedao import MovieDao
"""
@Author:XYT2000
@Content:通过用户名获取推荐的方法
"""
def getRecommendationByUser(collect):
    recommendationDao = RecommendationDao()
    movieDao = MovieDao()
    recommendList = []
    collectMovie = collect.split('-')
    for movieId in collectMovie:
        recommendMovieIds = (recommendationDao.getRecommendationByMovieId(str(movieId)))['recommendId'].split('-')
        for recommendMovieId in recommendMovieIds:
            recommenMovie =  movieDao.getMovieById(recommendMovieId)
            recommendList.append(recommenMovie)
    print(recommendList)

