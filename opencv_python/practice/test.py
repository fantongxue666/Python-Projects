import cv2
import matplotlib.pyplot as plt
import numpy as np

# 图像读取
def txcl():
    img = cv2.imread('D:\\tempFiles\\resources\\3.jpg', cv2.IMREAD_GRAYSCALE)
    # 图像的显示
    cv2.imshow("image", img)
    # 等待时间 毫秒级 0表示任意键终止
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(img.shape)
    print(type(img))
    print(img.size)
    print(img.dtype)

# 视频读取
def spdq():
    vc = cv2.VideoCapture('D:\\tempFiles\\resources\\hs.mp4') # 读取视频
  # 检查是否打开正确
    if vc.isOpened():
        open,frame = vc.read() # open：返回是否打开正确   frame：返回的每一帧图像
    else:
        open=False
    while open: # 打开正确时执行
        ret,frame = vc.read()
        if frame is None:
            break
        if ret == True:
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # 把每一帧处理成灰度图像
            cv2.imshow("result",gray) # 弹框展示视频
            if cv2.waitKey(10)&0xFF == 27: # 每一帧切换的速度是10
                break
    vc.release()
    cv2.destroyAllWindows()

# 图像融合
def txrh():
    tz_img = cv2.imread('D:\\tempFiles\\resources\\tz.jpg', cv2.IMREAD_COLOR)
    print(tz_img.shape) # (682, 1023, 3)
    jm = cv2.imread('D:\\tempFiles\\resources\\jm.jpg', cv2.IMREAD_COLOR)
    jm_img = cv2.resize(jm,(1023,682)) # 图像融合前提是形状得相同，不同就转换为相同的
    print(jm_img.shape)  # (682, 1023, 3)
    # 开始融合
    newImg = cv2.addWeighted(tz_img,0.5,jm_img,0.6,0)
    cv2.imshow("image", newImg)
    # 等待时间 毫秒级 0表示任意键终止
    cv2.waitKey(0)

# 阈值
def yz():
    tz_img = cv2.imread('D:\\tempFiles\\resources\\mm.png', cv2.IMREAD_GRAYSCALE)
    ret,thresh1 = cv2.threshold(tz_img,127,255,cv2.THRESH_TOZERO_INV)
    cv2.imshow("image",thresh1)
    cv2.waitKey(0)

# 腐蚀操作
def fscz():
    dg = cv2.imread('D:\\tempFiles\\resources\\dige2.png')
    kenel = np.ones((3,3),np.uint8)
    result = cv2.erode(dg,kenel,iterations=2) # 腐蚀之后的结果，线条没了，但是字变细了，现在再变粗
    # 膨胀操作
    result2 = cv2.dilate(result,kenel,iterations=2)

    cv2.imshow("image",result2)
    cv2.waitKey(0)

# 开运算和闭运算
def kyshbys():
    dg = cv2.imread('D:\\tempFiles\\resources\\dige2.png')
    kenel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(dg,cv2.MORPH_OPEN,kenel) # MORPH_OPEN：开运算  MORPH_CLOSED 闭操作
    cv2.imshow("image",opening)
    cv2.waitKey(0)

# 梯度运算
def tdys():
    dg = cv2.imread('D:\\tempFiles\\resources\\dige2.png')
    kenel = np.ones((5, 5), np.uint8)
    # 膨胀的结果
    result = cv2.dilate(dg, kenel, iterations=2)
    # 腐蚀的结果
    result2 = cv2.erode(dg, kenel, iterations=2)


    result3 = cv2.morphologyEx(dg,cv2.MORPH_GRADIENT,kenel)
    cv2.imshow("image", result3)
    cv2.waitKey(0)

# 梯度Sobel算子
def sobel():
    dg = cv2.imread('D:\\tempFiles\\resources\\dige.png')
    # 参数（图像，得出的结果保存负数的形式【否则会被截断为0】，横向计算，竖向不计算，方阵大小为3x3）
    new_dg = cv2.Sobel(dg,cv2.CV_64F,1,0,ksize=3)
    # 负数取绝对值
    abs = cv2.convertScaleAbs(new_dg)
    cv2.imshow("image",abs)
    cv2.waitKey(0)

def dny():
    dg = cv2.imread('D:\\tempFiles\\resources\\mm.png')
    down = cv2.pyrDown(dg) # 向下采样（变小）
    up = cv2.pyrUp(dg)  # 向上采样（变大）
    cv2.imshow("image", up)
    cv2.waitKey(0)

# 绘画轮廓
def hhlk():
    # 拿到原图
    dg = cv2.imread('D:\\tempFiles\\resources\\mm.png')
    # 转为灰度图
    gray = cv2.cvtColor(dg,cv2.COLOR_BGR2GRAY)
    # 灰度图转为二值化图
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    # 得到轮廓对象
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    # 把轮廓对象画出来
    drwo_dg = gray.copy()
    # 参数：传入图像，轮廓，轮廓索引（-1为画出全部轮廓），颜色，线条厚度
    res = cv2.drawContours(drwo_dg,contours,-1,(0,0,255),2)
    print("轮廓特征：\n",contours[1])
    print("轮廓面积：\n",cv2.contourArea(contours[1]))
    print("轮廓周长：\n",cv2.arcLength(contours[1],True)) # true代表闭合的轮廓
    # cv2.imshow("contours",res)
    # cv2.waitKey(0)
if __name__ == "__main__":
    hhlk()