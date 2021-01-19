import pymysql
import json

class BaseDao():

    def __init__(self, config="mysql.json"):
        self.__config = json.load(open(config)) # dict字典
        self.__connection = None
        self.__cursor = None
        pass

    def getConnection(self):
        print("成功连接数据库")
        if self.__connection != None:
            return self.__connection
        try:
            self.__connection = pymysql.connect(**self.__config)
            # 自动提交事务
            # self.__connection.autocommit(False) # 事务管理的开关
        except Exception as e:
            print("数据库连接失败：" +  str(e))
            pass
        return self.__connection
        

    def execute(self, sql, params=None, ret="tuple"):
        result = 0
        try:
            if ret == "dict":
                self.__cursor = self.getConnection().cursor(cursor=pymysql.cursors.DictCursor)
            else:
                self.__cursor = self.getConnection().cursor()
                pass
            if params:
                result = self.__cursor.execute(sql, params) # 返回的是条数
            else:
                result = self.__cursor.execute(sql)
        except Exception as e:
            print("数据库执行SQL语句出现异常：" + str(e))
            self.__connection.close()
            pass
        return result
        

    def commit(self):
        if self.__connection:
            self.__connection.commit()
            pass
        pass

    def rollback(self):
        if self.__connection:
            self.__connection.rollback()
            pass
        pass

    def close(self):
        if self.__connection !=None:
            self.__connection.close()
            pass
        if self.__cursor != None:
            self.__cursor.close()
            pass
        pass

    def fetchone(self):
        if self.__cursor != None:
            return self.__cursor.fetchone()
        pass

    def fetchall(self):
        if self.__cursor != None:
            return self.__cursor.fetchall()
        pass
    pass
