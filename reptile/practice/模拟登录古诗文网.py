# 需求，爬取csdn首页的全部html代码
import requests
from lxml import etree
def test():
    # 指定url古诗文网登录页
    url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
    # UA伪装
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }

    login_html=requests.get(url=url,headers=headers).text
    etreeObj = etree.HTML(login_html)
    # 找到验证码的标签，并复制xpath值
    yzm_src = "https://so.gushiwen.cn"+etreeObj.xpath('//*[@id="imgCode"]/@src')[0]
    # 请求验证码在线地址，得到二进制数据，并持久化到本地
    yzm_data = requests.get(url=yzm_src,headers=headers).content
    with open("yzm.jpg","wb") as tp:
        tp.write(yzm_data)

    yzm_value = input("验证码图片已下载，请输入验证码：")

    data={
        "__VIEWSTATE": "q5220JT0+dsek1Iq8Fjx0xFeucO6gCylR4IaiN5dDnXvRTA4UDtUG4oJlRrRML4jIcJ7LBp+bQgN/glEST9wTy81hdDS3DOcSZ5tYzDTwPn2Fa6Jqit2/GdazXs=",
        "__VIEWSTATEGENERATOR": "C93BE1AE",
        "from": "http://so.gushiwen.cn/user/collect.aspx",
        "email": "18838030468",
        "pwd": "aini12345",
        "code": yzm_value,
        "denglu": "登录"
    }

    # 创建session
    session = requests.session()
    # 登录url
    loginUrl = "https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx"

    print("正在模拟登录中。。。")
    response = session.post(url=loginUrl,data=data, headers=headers)
    if response.status_code==200:
        print("登录成功！开始爬取信息！")
        # 持久化登录成功后的html到本地
        with open('test.html','w',encoding='utf-8') as fp:
            fp.write(response.text)

        # 详情页的url
        xqUrl = "https://so.gushiwen.cn/user/collectbei.aspx?sort=t"
        # 然后就可以继续爬取详情页了（使用session发请求）


    else:
        print("模拟登录失败，请重试！")




if __name__=="__main__":
    test()

