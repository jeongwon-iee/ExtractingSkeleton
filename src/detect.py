
import cv2
import numpy as np
import json
from collections import OrderedDict

number = 0

cap = cv2.VideoCapture("../image/Test2.mp4")

# 옵션 설명 http://layer0.authentise.com/segment-background-using-computer-vision.html
#fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=0)
fgbg = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=0)

group_data = OrderedDict()
Data_set = OrderedDict()

while (number < 20):
    ret, frame = cap.read()

    width = frame.shape[1]
    height = frame.shape[0]
    frame = cv2.resize(frame, (int(width * 0.5), int(height * 0.5)))

    fgmask = fgbg.apply(frame)

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(fgmask)

    for index, centroid in enumerate(centroids):
        if stats[index][0] == 0 and stats[index][1] == 0:
            continue
        if np.any(np.isnan(centroid)):
            continue

        x, y, width, height, area = stats[index]
        centerX, centerY = int(centroid[0]), int(centroid[1])

        if area > 10:
            dst1 = fgmask.copy()
            dst1 = fgmask[y - 5:y + height + 5, x - 5:x + width + 5]
            dst2 = frame.copy()
            cv2.circle(dst2, (centerX, centerY), 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255))
            cv2.imwrite('../test/birds%d.png' % number, dst1)

            number = number + 1

    cv2.imshow('mask', fgmask)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

print()
print(stats[0][0], stats[0][1], stats[0][2], stats[0][3], stats[0][4])
print(stats[1][0], stats[1][1], stats[1][2], stats[1][3], stats[1][4])

cap.release()
cv2.destroyAllWindows()
