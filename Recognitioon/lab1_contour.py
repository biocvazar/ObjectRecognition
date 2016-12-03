from math import pi

__author__ = 'Bio'

import numpy as np
import cv2

image = cv2.imread('stones.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150, apertureSize = 3)


ret,thresh = cv2.threshold(gray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(image,contours,-1,(0,255,0),3)

cv2.imshow("fv", image)
cv2.waitKey()