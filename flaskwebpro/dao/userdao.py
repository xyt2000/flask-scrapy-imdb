from dao.basedao import BaseDao

# 实现规范用户信息的增删改查
class UserDao(BaseDao):
    # 查询操作
    def getUserByUserName(self, username):
        sql = "select * from t_user where username=%s"
        param = [username]
        result = self.execute(sql, param, ret="dict")
        return self.fetchone()
        pass

    # 修改
    def updateUserByUserId(self, param=[], id=0):
        sql = "update t_user set realname=%s, age=%s, phoneno=%s where id=%s"
        param.append(id)
        return self.execute(sql, param)
        pass

        # 修改

    def updateUser(self, param=[], id=0):
        sql = "update t_user set phoneno=%s, email=%s where id=%s"
        param.append(id)
        return self.execute(sql, param)
        pass

    def disableUserByUserId(self, id):
        sql = "update t_user set status=0 where id=%s"
        return self.execute(sql, [id])
        pass

    # 删除
    def removeUserByUserId(self, id):
        sql = "delete from t_user where id=%s"
        param = [id]
        return self.execute(sql, param)
        pass

    # 添加
    def createUser(self, param):
        sql = "insert into t_user (username, userpwd, realname, age, phoneno, email)" \
              "values (%s,%s,%s,%s,%s, %s )"
        return self.execute(sql, param)
        pass

    # 查找全部用户
    def getAllUserList(self):
        sql = "select * from t_user"
        self.execute(sql, ret="dict")
        return self.fetchall()
        pass

    def getUserListPage(self, paramDict):
        # 构造动态SQL语句
        sql = "select * from t_user where 1=1 "  # 1=1为了便于加查询条件
        params = []
        if paramDict.get("searchName"):
            sql += " and username like %s "
            params.append("%"+paramDict.get("searchName")+"%")
            pass
        sql += " limit %s, %s"
        startRow = (paramDict.get("currentPage") - 1) * paramDict.get('pageSize')
        params.append(startRow)
        params.append(paramDict.get('pageSize'))
        self.execute(sql, params, ret="dict")
        return self.fetchall()
        pass

    def getUserCounts(self, paramDict):
        # 构造动态SQL语句
        sql = "select count(*) as counts from t_user where 1=1 "  # 1=1为了便于加查询条件
        params = []
        if paramDict.get("searchName"):
            sql += " and username like %s"
            params.append("%" + paramDict.get("searchName") + "%")
            pass
        self.execute(sql, params, ret="dict")
        return self.fetchone()
        pass
    pass

