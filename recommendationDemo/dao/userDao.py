from .basedao import BaseDao

# 实现规范用户信息的增删改查
class UserDao(BaseDao):
    # 查询操作
    def getUserByUserName(self, username):
        sql = "select * from t_user where username=%s"
        param = [username]
        result = self.execute(sql, param, ret="dict")
        return self.fetchone()
        pass

    def getcommendationByUsername(self, username):
        sql = "select collectid from t_user where username = %s"
        param = [username]
        self.execute(sql, param, ret="dict")
        return self.fetchone()

    def setCollect(self,username,collect):
        sql = "update t_user set collectid = %s  where (username = %s)"
        param = [collect,username]
        print(collect)
        print(username)
        result = self.execute(sql, param, ret="dict")
        self.commit()
        return result
