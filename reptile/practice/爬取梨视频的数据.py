import requests
from lxml import etree
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
url = "https://www.pearvideo.com/category_5"
response = requests.get(url=url,headers=headers)
if response.status_code==200:
    etreeObj = etree.HTML(response.text)
    # 得到视频列表的li
    li_list = etreeObj.xpath('//*[@id="listvideoListUl"]/li')
    for li in li_list:
        detail_url = "https://www.pearvideo.com/"+li.xpath('.//a/@href')[0]
        # 这只是一个视频详情页的链接，并不是视频链接，要靠F12大胆的去发现，这里发现请求详情页后，又发了一个请求
        # https://www.pearvideo.com/videoStatus.jsp?contId=1718464&mrd=0.7595792109906241
        # 其中的contId就是detail_url参数的最后面的数字
        print(detail_url)
        name = li.xpath('.//div[@class="vervideo-title"]/text()')[0]+".mp4"
        print(name)
        # 截取字符串
        contId = detail_url[32:]
        # 请求视频详情页
        response = requests.get("https://www.pearvideo.com/videoStatus.jsp?contId="+contId+"&mrd=0.7595792109906241")
        if response.status_code==200:
            # 得到视频真实地址
            jsons=response.json()
            react_url = jsons["videoInfo"]["videos"]["srcUrl"]
            print("视频真实地址：",react_url)


