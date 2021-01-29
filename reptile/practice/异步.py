import requests
# 导入线程池模块所需要的类
from multiprocessing.dummy import Pool
urls = [
    "http://disk.tiger2.cn/FastDFS/libfastcommonV1.0.7.tar.gz",
    "http://disk.tiger2.cn/FastDFS/FastDFS_v5.05.tar.gz",
    "http://disk.tiger2.cn/FastDFS/fastdfs_client_java._v1.25.tar.gz"
]
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }

def getContent(url):
    print("正在爬取："+url)
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        print("响应数据长度为：",len(response.content))

# 实例化一个线程池对象
pool = Pool(4)
# 将列表中每一个列表元素传递给getContent方法进行处理（异步）
pool.map(getContent,urls)