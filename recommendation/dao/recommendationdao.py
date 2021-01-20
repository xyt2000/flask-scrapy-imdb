from .basedao import BaseDao

class  RecommendationDao(BaseDao):
    def insertRecommend(self, params):
        sql = "insert into t_recommend (movieId, recommendId) values ( % s, % s)"
        self.execute(sql, params,ret = "dict")
    pass

    def findAllRecommend(self):
        self.execute("select * from t_recommend",ret="dict")
        return self.fetchall()

    def getRecommendationByMovieId(self,params):
        sql = "select recommendId from t_recommend where movieId = %s"
        self.execute(sql, params, ret="dict")
        return self.fetchone()