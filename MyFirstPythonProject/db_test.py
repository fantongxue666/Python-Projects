import pymysql
server = "127.0.0.1"
user = "root"
password = "1234"
db="test"
# 连接数据库
conn = pymysql.connect(server, user, password, database=db) # 获取连接
cursor = conn.cursor() # 获取游标
# "**ENGINE=InnoDB DEFAULT CHARSET=utf8**"-创建表的过程中增加这条，中文就不是乱码

# 查询数据库表user内容
cursor.execute("SELECT * FROM stu")
# row = cursor.fetchone() # 查看一行
row = cursor.fetchall() # 查看多行
# print(row)
