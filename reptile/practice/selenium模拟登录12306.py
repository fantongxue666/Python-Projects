from selenium import webdriver
import time
#导入动作链对应的类
from selenium.webdriver import ActionChains
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
# 因为我个人电脑的原因，屏幕缩放比例是125%，所以都乘以1.25
range = (
    int(location['x']*1.25),int(location['y']*1.25),int((location['x']+size['width'])*1.25),int((location['y']+size['height'])*1.25)
)
# 至此，验证码图片区域进行图片裁剪
i = Image.open('./aa.png')
# crop根据指定区域进行图片裁剪
frame = i.crop(range)
# 保存截图到当前目录
frame.save('./code.png')

# 比如通过超级鹰在线接口返回了坐标信息，我们对坐标信息进行数据处理，处理成了[[253,23],[267,25]]   （两个坐标）
list = [[253,23],[267,25]]
# 遍历列表，使用动作链对每一个列表元素对应的x,y指定的位置进行模拟点击
for l in list:
    x = l[0]
    y = l[1]
    # 这个x,y坐标只是相对于code.png这张图片来说的，但是模拟点击要得到这个验证码图片要点击的内容的坐标是相对于浏览器的，所以用动作链来切换为浏览器的坐标
    ActionChains(bro).move_to_element_with_offset(code_img_ele,x,y).click().perform()
    time.sleep(1)
#录入用户名和密码，并点击登录确认按钮
bro.find_element_by_id('username').send_keys('xxx')
bro.find_element_by_id('password').send_keys('xxx')
bro.find_element_by_id('login').click()
print('模拟登录成功')
bro.quit()
