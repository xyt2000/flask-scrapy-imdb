from flask import Blueprint, jsonify, request
from dao.jobdao import JobDao

datacontroller = Blueprint('datacontroller', __name__)

@datacontroller.route('/getjobtypesalary', methods=['GET', 'POST'])
def getJobTypeSalary():
    # 方法接受的是AJAX请求
    jobDao = JobDao()
    data = jobDao.statisticJobTypeAvgSalary()
    return jsonify(data)
    pass

@datacontroller.route('/getcityjobcount', methods=['GET', 'POST'])
def getCityJobCount():
    # 方法接受的是AJAX请求
    jobDao = JobDao()
    data = jobDao.statisticCityJobCount()
    return jsonify(data)
    pass
