from SQLDAO import SQLDAO
from NetInfo import interface
from Config import sqlConnection

# 获取数据并插入数据库
def buildSQL():
    sql = SQLDAO(sqlConnection['url'], sqlConnection['username'], sqlConnection['password'])
    sql.insertInfo(interface.getData())

# buildSQL()