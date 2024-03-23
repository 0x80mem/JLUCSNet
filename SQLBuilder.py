from SQLDAO import SQLDAO
import interface
from Config import sqlConnection
import CollegeInfo
import Construct
import Party
import PerTraining
import PublicNote
import Recuit
import Scisearch
import TeachersInfo
import TestCenter
import interface

# 获取数据并插入数据库
def buildSQL():
    sql = SQLDAO(sqlConnection['url'], sqlConnection['user'], sqlConnection['password'])
    sql.clearAll()
    works = [Recuit.work, CollegeInfo.work, Construct.work, Party.work, PerTraining.work, PublicNote.work,
            Scisearch.work, TeachersInfo.work, TestCenter.work]
    for work in works:
        sql.insertInfo(interface.catchWork(work))

buildSQL()