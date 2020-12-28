from flask import Flask, request, session
from flask import render_template
app = Flask(__name__)
app.config['SECRET_KEY']='123456'
app.secret_key='123456'
from flask import redirect
from utils.DBHandle import DataBaseHandle
import json,uuid,datetime
from utils.DateEncoder import DateEncoder
# from bank.db_test import newRoute
# newRoute(app)
@app.route('/')
def hello_world():
  return redirect('index')

@app.route('/addArticle')
def addArticle():
    return render_template('addArticle.html')

@app.route('/index')
def toIndex():
    account=session.get('account')
    tags=''
    if account!=None:
        sql = "select tags from user where account = '%s'" % (account)
        data = DataBaseHandle().selectDB(sql)
        tags = data[0][0]
    else:
        tags='请先登录！'
    return render_template('index.html',tags=tags)

@app.route('/login')
def toLogin():
    return render_template('login.html')

@app.route('/saveArticle',methods=['POST'])
def saveArticle():
    title = request.form.get('title')
    content = request.form.get('content')
    test = request.form.get('test')
    account=session.get("account")
    if test!='':
        sql="select tags from user where account = '%s'" % (account)
        data = DataBaseHandle().selectDB(sql)
        tags=data[0][0]
        if tags!=None:
            newTest = tags + ',' + test
            sql2 = "update user set tags = '%s' where account ='%s'" % (newTest, account)
            DataBaseHandle().updateDB(sql2)
        else:
            sql2 = "update user set tags = '%s' where account ='%s'" % (test, account)
            DataBaseHandle().updateDB(sql2)

    id=uuid.uuid1()
    username=session.get("username")
    nowDate=datetime.datetime.now()
    sql="insert into article values('%s','%s','%s','%s','%s','%s')" % (id,title,content,account,username,nowDate)
    i = DataBaseHandle().updateDB(sql)
    if i>0:
        return 'success'
    else:
        return 'error'

# 查询评论
@app.route('/getPinglun',methods=['POST'])
def getPinglun():
    articleid = request.form.get('articleid')
    sql="SELECT b.username,a.content,a.time FROM pinglun a LEFT JOIN user b ON b.account = a.fromaccount WHERE articleid = '%s' order by a.time ASC" % (articleid)
    data = DataBaseHandle().selectDB(sql)
    list=[]
    for obj in data:
        list.append({
            'username':obj[0],
            'content':obj[1],
            'time':obj[2]
        })
    return json.dumps(list,cls=DateEncoder)

# 发表评论
@app.route('/pinglun',methods=['POST'])
def pinglun():
    id=uuid.uuid1()
    fromaccount=session.get('account')
    toaccount=request.form.get('toaccount')
    content=request.form.get('content')
    time=datetime.datetime.now()
    articleid=request.form.get('articleid')
    sql="insert into pinglun(id,fromaccount,toaccount,content,time,articleid) values('%s','%s','%s','%s','%s','%s')" % (id,fromaccount,toaccount,content,time,articleid)
    i = DataBaseHandle().updateDB(sql)
    if i>0:
        return 'success'
    else:
        return 'error'

# 博客详情页
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
    bs = int(request.form.get('bs'))
    sql=""
    if bs==1:
        sql="select * from article order by time desc"
    elif bs ==2:
        account = session.get('account')
        sql="select * from article where account='%s' order by time desc" % (account)
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
    session["account"] = None
    tags = '请先登录！'
    return render_template('index.html', tags=tags)

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
        session["tags"] = data[0][4]
        return '登录成功'
    else:
        return '登录失败'


if __name__ == '__main__':
    app.run()
