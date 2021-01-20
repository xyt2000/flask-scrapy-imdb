from .basedao import BaseDao

class UserDao(BaseDao):
    def getcommendationByUsername(self, username):
        sql = "select collectid from t_user where username = %s"
        param = [username]
        self.execute(sql, param, rey="dict")
        return self.fetchone()

