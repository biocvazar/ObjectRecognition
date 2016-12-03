import cv2
import numpy as np

cap = cv2.VideoCapture('ball.avi')

number_of_frames = cap.get(7)
ret, back = cap.read()
row, col, chanel = np.shape(back)
back_gr = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)

background = np.zeros((row, col), np.uint8)

print(back_gr)
for _ in range(int(cap.get(5))//2):
    ret2, back = cap.read()
    ret, frame = cap.read()
    if ret and ret2:
        frame_gr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        back_gr= cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
        diff = abs(frame_gr - back_gr)
        if diff.all() < 5:
            background = frame_gr[np.where(diff < 5)]
            if diff.all() < 20:
                background = frame_gr[np.where(diff < 20)]
        else:
            background = (frame_gr[np.where(diff < 20)] + back_gr[np.where(diff < 20)])/2
        back_gr = frame_gr

cv2.imshow("bg", background)
cv2.waitKey()

cap.release()
cv2.destroyAllWindows()