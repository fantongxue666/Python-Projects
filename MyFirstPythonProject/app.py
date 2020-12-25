from flask import Flask
from flask import render_template
app = Flask(__name__)
import json
from DBHandle import DataBaseHandle


@app.route('/')
def hello_world():
    db = DataBaseHandle()  # 数据库操作类 全局
    data = db.selectDB("select * from stu")
    return json.dumps(data)

@app.route('/index')
def toIndex():
    title='樊同学的'
    user={'username':'樊同学'}
    return render_template('index.html',title=title,user=user)

if __name__ == '__main__':
    app.run()
