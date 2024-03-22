import CollegeInfo
import Construct
import Party
import PerTraining
import PublicNote
import Recuit
import Scisearch
import TeachersInfo
import TestCenter


def getData():
    works = [Recuit.work, CollegeInfo.work, Construct.work, Party.work, PerTraining.work, PublicNote.work,
            Scisearch.work, TeachersInfo.work, TestCenter.work]
    dics = []
    for work in works:
        dics.append(catchWork(work))


def catchWork(work,count = 0):
    try:
        return work()
    except:
        if count >=5:
            raise 'beyond'
        catchWork(work,count+1)


getData()
