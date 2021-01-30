from selenium import webdriver
from lxml import etree
import time
# 实例化一个浏览器对象（传入浏览器的驱动程序chromedriver.exe）
bro = webdriver.Chrome(executable_path='./chromedriver.exe')
# 让浏览器发起一个指定url对应请求
bro.get('https://www.taobao.com/')
# 标签定位
search_input = bro.find_element_by_id('q')
# 标签交互（向输入框输入内容）
search_input.send_keys('IPhone')
# 执行一组js程序（向下滚动一个屏幕的距离）
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# 点击按钮
btn = bro.find_element_by_css_selector('.btn-search')
btn.click()
time.sleep(5)
bro.quit()
