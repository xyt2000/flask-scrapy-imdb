import os
import time
import sched
import smtplib


schedule = sched.scheduler(time.time, time.sleep)
password = '070500'

def backupsDB():

    cmdString = 'D:/mysql/mysql-8.0.15-winx64/bin/mysqldump -hlocalhost -P3306 -u root -p'+password+' db_movie_info > C:/Users/xytbu/scrapy-imdb/flask-scrapy-imdb/db_movie_info.sql'
    os.system(cmdString)

def perform_command(cmd, inc):
    # 安排inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    os.system(cmd)
    backupsDB()

def timming_exe(cmd, inc=10):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()

if __name__ == '__main__':
    print("show time after 10 seconds:")
    timming_exe("echo %time%", 10)
