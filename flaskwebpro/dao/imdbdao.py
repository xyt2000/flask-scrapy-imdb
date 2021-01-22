from dao.basedao import BaseDao

class ImdbDao(BaseDao):

    def getImdbPage(self,paramDict):
        sql = "select * from imdb_data where 1=1 "  # 1=1为了便于加查询条件
        params = []
        if paramDict.get("searchName"):
            sql += " and title like %s "
            params.append("%" + paramDict.get("searchName") + "%")
            pass
        sql += " limit %s, %s"
        startRow = (paramDict.get("currentPage") - 1) * paramDict.get('pageSize')
        params.append(startRow)
        params.append(paramDict.get('pageSize'))
        self.execute(sql, params, ret="dict")
        return self.fetchall()
        pass

    def getImdbCounts(self, paramDict):
        # 构造动态SQL语句
        sql = "select count(*) as counts from imdb_data where 1=1 "  # 1=1为了便于加查询条件
        params = []
        if paramDict.get("searchName"):
            sql += " and username like %s"
            params.append("%" + paramDict.get("searchName") + "%")
            pass
        self.execute(sql, params, ret="dict")
        return self.fetchone()
        pass

    def statisticGenresCounts(self):
        sql = "select genres,count(*) as num from imdb_data group by genres"
        self.execute(sql, ret='dict')
        return self.fetchall()
        pass

    def statisticYearCounts(self):
        sql="select release_date,count(*) as s from imdb_data group by release_date"
        self.execute(sql,ret='dict')
        return self.fetchall()
        pass

    def statisticRateCounts(self):
        sql="select rating,count(*) as s from imdb_data group by rating"
        self.execute(sql,ret='dict')
        return self.fetchall()
        pass

    def statisticMetaScoreCounts(self):
        sql = "select metascore,count(*) as s from imdb_data group by metascore"
        self.execute(sql, ret='dict')
        return self.fetchall()
        pass

    def statisticDurationCounts(self):
        sql = "select duration,count(*) as s from imdb_data group by duration"
        self.execute(sql, ret='dict')
        return self.fetchall()
        pass

    def statisticTop5(self):
        sql="select * from (select * from imdb_data order by cumulative_worldwide_gross DESC) as a limit 5"
        self.execute(sql,ret='dict')
        return self.fetchall()
        pass

    pass