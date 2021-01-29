import requests

if __name__ == "__main__":
    url = "https://www.baidu.com/s?wd=ip"
    # UA伪装
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    response = requests.get(url=url,headers=headers,proxies={"https":"222.110.147.50:3128"})
    with open("test.html","w",encoding="utf-8") as fp:
        fp.write(response.text)