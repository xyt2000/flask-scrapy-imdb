from dao.basedao import BaseDao

class JobDao(BaseDao):

    def createJobData(self, param):
        sql = "insert into t_jobdata (jobname, jobcompany, jobaddress," \
              "jobsalary,jobdate,joblink,jobcity, lowsalary, highsalary, meansalary, jobtype) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        return self.execute(sql, param)
        pass

    # 使用SQL语句来统计分析数据：聚合函数
    def statisticJobTypeAvgSalary(self):
        sql = "select avg(meansalary) as s, jobtype from t_jobdata group by jobtype"
        self.execute(sql, ret='dict')
        return self.fetchall()
        pass

    def statisticJobTypeJobCount(self):
        sql = "select count(*) as s, jobtype from t_jobdata group by jobtype"
        self.execute(sql, ret='dict')
        return self.fetchall()
        pass

    def statisticCityJobCount(self):
        sql = "select count(*) as value, jobcity as name from t_jobdata group by jobcity"
        self.execute(sql, ret='dict')
        return self.fetchall()
        pass

    def getJobList(self):
        sql = "select * from t_jobdata"
        self.execute(sql, ret='dict')
        return self.fetchall()
        pass
    pass