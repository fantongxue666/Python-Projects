from flask import Flask, request, session
from flask import render_template
app = Flask(__name__)
app.config['SECRET_KEY']='123456'
app.secret_key='123456'
from flask import redirect
from utils.DBHandle import DataBaseHandle
import json,uuid,datetime
from utils.DateEncoder import DateEncoder
from practice.db_test import newRoute
newRoute(app)
@app.route('/')
def hello_world():
  return redirect('index')

@app.route('/addArticle')
def addArticle():
    return render_template('addArticle.html')

@app.route('/index')
def toIndex():
    return render_template('index.html')

@app.route('/login')
def toLogin():
    return render_template('login.html')

@app.route('/saveArticle',methods=['POST'])
def saveArticle():
    title = request.form.get('title')
    content = request.form.get('content')
    id=uuid.uuid1()
    account=session.get("account")
    username=session.get("username")
    nowDate=datetime.datetime.now()
    sql="insert into article values('%s','%s','%s','%s','%s','%s')" % (id,title,content,account,username,nowDate)
    i = DataBaseHandle().updateDB(sql)
    if i>0:
        return 'success'
    else:
        return 'error'

@app.route('/getArticleById',methods=['GET'])
def getArticleById():
    id = request.args.get('id')
    sql="select * from article where id = '%s'" % (id)
    data = DataBaseHandle().selectDB(sql)
    newData = data[0]
    obj={
        "id":newData[0],
        "title":newData[1],
        "content":newData[2],
        "account":newData[3],
        "username":newData[4],
        "time":newData[5]
    }

    return render_template('article_detail.html',obj=obj)

# 查询所有文章
@app.route('/getAllArticles',methods=['POST'])
def getAllArticles():
    sql="select * from article order by time desc"
    data = DataBaseHandle().selectDB(sql)
    list=[]
    for obj in data:
        list.append({
            'id': obj[0],
            'title': obj[1],
            'content': obj[2],
            'account': obj[3],
            'username': obj[4],
            'time': obj[5]
        })
    return json.dumps(list,cls=DateEncoder)

# 退出
@app.route('/logout')
def logout():
    session["username"]=None
    return render_template('index.html')

# # 判断是否登录
@app.route('/isLogin',methods=['POST'])
def isLogin():
    name = session.get("username")
    if name!=None:
        return name
    else:
        return '没有登录'

# 登录接口
@app.route('/denglu',methods=['POST'])
def denglu():
    account=request.form.get('account')
    pwd=request.form.get('pwd')
    # 查询用户
    sql="select * from user where account='%s' and pwd ='%s'" % (account,pwd)
    db = DataBaseHandle()
    data = db.selectDB(sql)
    if len(data) > 0:
        # 记录登录状态
        session["username"] = data[0][3]
        session["account"] = data[0][1]
        return '登录成功'
    else:
        return '登录失败'


if __name__ == '__main__':
    app.run()
