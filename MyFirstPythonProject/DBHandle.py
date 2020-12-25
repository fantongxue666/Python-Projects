import pymysql
class DataBaseHandle(object):
    # 相当于java的构造方法，初始化数据库信息并创建数据库连接
    def __init__(self):
        self.host = '127.0.0.1'
        self.username = 'root'
        self.password = '1234'
        self.database = 'test'
        self.db = pymysql.connect(self.host, self.username, self.password, self.database)

    # 增删改
    def updateDB(self,sql):
        cursor = self.db.cursor()
        try:
            i = cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            cursor.close()
        return i

    # 查询
    def selectDB(self,sql):
        cursor = self.db.cursor()
        temp = None
        try:
            cursor.execute(sql)
            temp = cursor.fetchall() # 返回所有记录列表
        except:
            print("查询发生错误")
        finally:
            self.db.close()
        return temp