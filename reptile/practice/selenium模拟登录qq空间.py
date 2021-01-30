from selenium import webdriver
import time
# 无可视化界面
from selenium.webdriver.chrome.options import Options
# 实现规避检测
from selenium.webdriver import ChromeOptions
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
# 创建一个参数对象，用来控制chrome以无界面模式打开
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 实例化一个浏览器对象（传入浏览器的驱动程序chromedriver.exe）
bro = webdriver.Chrome(executable_path='./chromedriver.exe',chrome_options=chrome_options,options=option)
# 让浏览器发起一个指定url对应请求
bro.get('https://qzone.qq.com/')
bro.switch_to.frame('login_frame')# 值是iframe的id值
# 获取登录链接标签
loginButton = bro.find_element_by_id('switcher_plogin')
# 点击
loginButton.click()
# 账号输入框
account_input = bro.find_element_by_id('u')
# 密码输入框
pwd_input = bro.find_element_by_id('p')
# 输入账号和密码
account_input.send_keys('675361896')
pwd_input.send_keys('*******')
# 点击登录
login = bro.find_element_by_id('login_button')
login.click()
time.sleep(5)
bro.quit()
