import scrapy

from reptile.scrapyTest.scrapyTest.items import ScrapytestItem


class SpidernameSpider(scrapy.Spider):
    name = 'spiderName'
    # 允许爬取的域名（如果遇到非该域名的url则爬取不到数据）
    allowed_domains = ['https://www.qiushibaike.com']
    # 起始爬取的url
    start_urls = ['https://www.qiushibaike.com/']

    # 访问起始URL并获取结果后的回调函数，该函数的response参数就是向起始的url发送请求后，获取的响应对象.该函数返回值必须为可迭代对象或者NUll
    def parse(self, response):
        # xpath为response中的方法，可以将xpath表达式直接作用于该函数中
        odiv = response.xpath('//*[@id="content"]/div/div[2]/div/ul/li')
        content_list = []  # 用于存储解析到的数据
        for div in odiv:
            # xpath函数返回的为列表，列表中存放的数据为Selector类型的数据。我们解析到的内容被封装在了Selector对象中，需要调用extract()函数将解析的内容从Selecor中取出。
            author = div.xpath('.//a[@class="recmd-content"]/text()')[0].extract()
            # 将解析到的数据封装至items对象中
            item = ScrapytestItem()
            item['author'] = author
            yield item  # 提交item到管道文件（pipelines.py）
