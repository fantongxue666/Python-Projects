from selenium import webdriver
#导入动作链对应的类
from selenium.webdriver import ActionChains

# 实例化一个浏览器对象（传入浏览器的驱动程序chromedriver.exe）
bro = webdriver.Chrome(executable_path='./chromedriver.exe')
# 让浏览器发起一个指定url对应请求
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
# 如果定位的标签是存在与iframe中则必须通过如下操作再进行标签定位
bro.switch_to.frame('iframeResult')# 切换浏览器标签定位的作用域
# 获取拖动小滑块的div元素
div = bro.find_element_by_id('draggable')
# 动作链
action = ActionChains(bro)
# 点击长按指定的标签（滑块）
action.click_and_hold(div)
for i in range(5):
    # perform立即执行动作链操作
    # move_by_offset(x,y)：x：水平方向 y：竖直方向
    action.move_by_offset(17,0).perform()
# 释放动作链
action.release()
bro.quit()
