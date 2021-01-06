import cv2
from imutils.perspective import four_point_transform
import pytesseract
import os
from PIL import Image
import argparse
import matplotlib as plt
import numpy as np

def order_points(pts):
	# 初始化4个坐标点的矩阵
	rect = np.zeros((4, 2), dtype = "float32")

	# 按顺序找到对应坐标0123分别是 左上，右上，右下，左下
	# 计算左上，右下
	print("pts :\n ",pts)
	s = pts.sum(axis = 1)		# 沿着指定轴计算第N维的总和
	print("s : \n",s)
	rect[0] = pts[np.argmin(s)]	# 即pts[1]
	rect[2] = pts[np.argmax(s)]	# 即pts[3]
	print("第一次rect : \n",rect)
	# 计算右上和左下
	diff = np.diff(pts, axis = 1)	# 沿着指定轴计算第N维的离散差值
	print("diff : \n",diff)
	rect[1] = pts[np.argmin(diff)]	# 即pts[0]
	rect[3] = pts[np.argmax(diff)]	# 即pts[2]
	print("第二次rect :\n ",rect)
	return rect

def four_point_transform(image, pts):
	# 获取输入坐标点
	rect = order_points(pts)
	(A, B, C, D) = rect
	# (tl, tr, br, bl) = rect

	# 计算输入的w和h值
	w1 = np.sqrt(((C[0] - D[0]) ** 2) + ((C[1] - D[1]) ** 2))
	w2 = np.sqrt(((B[0] - A[0]) ** 2) + ((B[1] - A[1]) ** 2))
	w = max(int(w1), int(w2))

	h1 = np.sqrt(((B[0] - C[0]) ** 2) + ((B[1] - C[1]) ** 2))
	h2 = np.sqrt(((A[0] - D[0]) ** 2) + ((A[1] - D[1]) ** 2))
	h = max(int(h1), int(h2))

	# 变换后对应坐标位置
	dst = np.array([	# 目标点
		[0, 0],
		[w - 1, 0],	# 防止出错,-1
		[w - 1, h - 1],
		[0, h - 1]], dtype = "float32")

	# 计算变换矩阵	(平移+旋转+翻转),其中
	M = cv2.getPerspectiveTransform(rect, dst)	# (原坐标,目标坐标)
	print(M,M.shape)
	warped = cv2.warpPerspective(image, M, (w, h))

	# 返回变换后结果
	return warped


# 绘图展示
def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 读取文档图像
image = cv2.imread("D:\\tempFiles\\resources\\doc.jpg")
# resize 坐标也会相同变化
ratio = image.shape[0] / 500.0
cv_show("原图", ratio)
orig = image.copy()
image=cv2.resize(orig,None,fx=0.2,fy=0.2)
	# 同比例变化：h指定500,w也会跟着变化
# 预处理
# 灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 去噪声
gray = cv2.GaussianBlur(gray, (5, 5), 0)
# 边缘检测
edged = cv2.Canny(gray, 75, 200)
cv_show("边缘检测",edged)
# 轮廓检测
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
# cnts中可检测到许多个轮廓,取前5个最大面积的轮廓
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# 遍历轮廓
for c in cnts:	# C表示输入的点集
	# 计算轮廓近似
	peri = cv2.arcLength(c, True)
	# epsilon表示从原始轮廓到近似轮廓的最大距离，它是一个准确度参数
	# True表示封闭的
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	print(approx,approx.shape)
	# 4个点的时候就拿出来,screenCnt是这4个点的坐标
	if len(approx) == 4:	# 近似轮廓得到4个点,意味着可能得到的是矩形
		screenCnt = approx	# 并且最大的那个轮廓是很有可能图像的最大外围
		break
# 画轮廓
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv_show("画轮廓",image)

# 透视变换
# 4个点的坐标 即4个(x,y),故reshape(4,2)
# 坐标是在变换后的图上得到,要还原到原始的原图上,需要用到ratio
print(screenCnt.shape)
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
wraped=cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
ref=cv2.threshold(wraped,100,255,cv2.THRESH_BINARY)[1]
ref=cv2.resize(ref,None,fx=0.3,fy=0.3)
cv_show("test",ref)

