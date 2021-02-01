# start.py
from scrapy.cmdline import execute

# 将命令的每个单词存进一个列表传给execute()
execute(['scrapy', 'crawl', 'spiderName', '--nolog',' -o','xxx.csv'])	# 相当于在终端输入命令
