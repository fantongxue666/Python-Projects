
class ScrapytestPipeline:
    # 构造方法
    def __init__(self):
        self.fp = None  # 定义一个文件描述符属性

    # 下列都是在重写父类的方法：
    # 开始爬虫时，执行一次
    def open_spider(self, spider):
        print('爬虫开始')
        self.fp = open('./data.txt', 'w')

    # 因为该方法会被执行调用多次，所以文件的开启和关闭操作写在了另外两个只会各自执行一次的方法中。
    def process_item(self, item, spider):
        # 将爬虫程序提交的item进行持久化存储
        self.fp.write(item['author']  + '\n')
        return item

    # 结束爬虫时，执行一次
    def close_spider(self, spider):
        self.fp.close()
        print('爬虫结束')
