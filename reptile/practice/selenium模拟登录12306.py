from selenium import webdriver
import time
# 用于裁剪
from PIL import Image

bro = webdriver.Chrome(executable_path='./chromedriver.exe')
# 浏览器全屏放大
bro.maximize_window()
# 让浏览器发起一个指定url对应请求
bro.get('https://kyfw.12306.cn/otn/resources/login.html')
time.sleep(1)
zhdl = bro.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a')
zhdl.click()
time.sleep(2)
# save_screenshot就是将当前页面进行截图并保存
bro.save_screenshot('aa.png')
# 确定验证码图片对应的左上角和右下角的坐标（确定裁剪的区域）  这个xpath可以在F12中找到验证码div元素右键copy->xpath
code_img_ele = bro.find_element_by_id('J-loginImg')
# 验证码div元素左上角的坐标
location = code_img_ele.location
print(location)
# 验证码div元素对应长和高
size = code_img_ele.size
print(size)
# 左上角和右下角坐标
range = (
    int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])
)
# 至此，验证码图片区域进行图片裁剪
i = Image.open('./aa.png')
# crop根据指定区域进行图片裁剪
frame = i.crop(range)
# 保存截图到当前目录
frame.save('./code.png')

bro.quit()
