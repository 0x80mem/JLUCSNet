import CollegeInfo
import Construct
import Party
import PerTraining
import PublicNote
import Recuit
import Scisearch
import TeachersInfo
import TestCenter
import time

INITIAL_INTERVAL = 1
MAX_ATTEMPTS = 3

def insertInfo(info):
    print(info)
def getData():
    works = [Recuit.work, CollegeInfo.work, Construct.work, Party.work, PerTraining.work, PublicNote.work,
            Scisearch.work, TeachersInfo.work, TestCenter.work]
    #dics = []
    for work in works:
        #dics.append(catchWork(work))
        insertInfo(catchWork(work))#获得的每页内容直接存储


def catchWork(work, interval=INITIAL_INTERVAL, attempts=MAX_ATTEMPTS):
    try:
        data = work()
        interval /= 2
        return data
    except :
        print("网络波动，连接失败！")
        if attempts > 0:
            print(f"重试中...，剩余尝试次数: {attempts}")
            time.sleep(interval)
            return catchWork(work, interval * 2, attempts - 1)
        else:
            print("已达到最大尝试次数")
            return None

getData()
