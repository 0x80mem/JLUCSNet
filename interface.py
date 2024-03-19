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
    dics = [Recuit.work(), CollegeInfo.work(), Construct.work(), Party.work(), PerTraining.work(), PublicNote.work(),
            Scisearch.work(), TeachersInfo.work(), TestCenter.work()]
    return dics
