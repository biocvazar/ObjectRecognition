__author__ = 'Bio'

import cv2
import numpy as np

cap = cv2.VideoCapture('video_car.mp4')

start = int(183)
end = int(188)
step = (end - start) // 5

frame_indexes = []
for i in range(start, end, step):
    cap.set(cv2.CAP_PROP_POS_MSEC, i*1000)
    ret, frame = cap.read()
    cv2.imwrite('car_frame_%d' % i + '.jpg', frame)
    frame_indexes.append(i)
cap.release()

images = []
names = []
for i in frame_indexes:
    images.append(cv2.imread('car_frame_%d' % i + '.jpg'))
    names.append('car_frame_%d' % i + '.jpg')

# images_data = []
# for image, i in zip(images, range(len(images))):
#     height, width, chanel = np.shape(image)
#     images_data.append({'name':names[i], 'width':width, 'height':height, 'chanel':chanel})
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite('gray_' + names[i], gray)


# print(images_data)

# median = cv2.medianBlur(images[0], 5)
# cv2.imshow('Without filters', images[0])
# cv2.imshow('With median filter', median)
# cv2.waitKey()


gray1 = cv2.cvtColor(images[2], cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(images[3], cv2.COLOR_BGR2GRAY)
height1, width1 = np.shape(gray1)
height2, width2 = np.shape(gray2)
zh, zw = 5, 5
MIN = []
min_dif = []
for i in range(zh):
    for j in range(zw):
        dif = gray1[5 - i:-i][5 - j:-j] - gray2[5 - i:-i][5 - j:-j]
        dif_sum = dif.sum()
        MIN.append((dif_sum, dif))

for difs in MIN:
    value = 10**100
    summ , dif = difs
    if summ < value:
        value = summ
        min_dif = dif

cv2.imshow('1', gray1)
cv2.imshow('2', gray2)
cv2.imshow('min', min_dif)
cv2.waitKey()