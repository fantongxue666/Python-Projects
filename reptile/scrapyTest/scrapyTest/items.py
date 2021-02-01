# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    author = scrapy.Field() #存储作者
    print("在items.py接收到的标题",author)
    pass
