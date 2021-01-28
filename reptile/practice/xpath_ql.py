# 需求，爬取csdn首页的全部html代码
import requests
from lxml import etree
def test():
    # 指定url
    url = "https://blogs.qianlongyun.cn/page/"
    # UA伪装
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }

    # 发起请求
    for i in range(12):
        print("========== 当前爬取页面：第"+str(i)+"页 ==============")
        newUrl = url+str(i+1)+"/"
        response = requests.get(url=newUrl, headers=headers)
        # 得到etree对象
        etreeObj = etree.HTML(response.text)
        # 得到所有文章的div
        articles = etreeObj.xpath("//div[@class='content']/article")
        for article in articles:
            print("========================")
            # 拿到文章标题
            content = article.xpath(".//h2/a/text()")[0]
            print("博客标题："+content)
            imgUrl = article.xpath(".//img/@src")[0]
            print("博客配图在线链接：" + imgUrl)
            author = article.xpath("./p[1]/span[1]/text()")[0]
            print("作者：" + author)



if __name__=="__main__":
    test()

