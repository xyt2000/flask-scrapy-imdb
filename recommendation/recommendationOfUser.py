from dao.recommendationdao import RecommendationDao
from dao.moviedao import MovieDao
def getRecommendationByUser(collect):
    recommendationDao = RecommendationDao()
    movieDao = MovieDao()
    recommendList = []
    collectMovie = collect.split('-')
    for movieId in collectMovie:
        recommendMovieIds = (recommendationDao.getRecommendationByMovieId(str(movieId)))['recommendId'].split('-')
        for recommendMovieId in recommendMovieIds:
            recommenMovie =  movieDao.getMovieById(Id)
            recommendList.append(recommenMovie)
    print(recommendList)

getRecommendationByUser('1-2')
