import math
import vector_extractor as v_e
import test

def read_vectors():

     theta =-3.0979594
     v = v_e.get_vectors("../image/black.png", theta)
     center = v.center
     head = v.head
     tail = v.tail
     wing1 = v.wing1
     wing2 = v.wing2

     vec= (head.x-center.x, head.y-center.y) #기준벡터: 머리-중심
     vec1= (wing1.x-center.x, wing1.y-center.y) #날개벡터 1
     vec2= (wing2.x-center.x, wing2.y-center.y) #날개벡터 2

     if (vec==(0,0)): #for front-rear frame
          return read_front_vectors(vec1, vec2)
     
     isClockWise = 1 #시계방향
     if (head.x > tail.x): isClockWise= 0 #반시계방향
     
     theta1= CalAngleBetweenTwoPoints(vec, vec1, isClockWise)
     theta2= CalAngleBetweenTwoPoints(vec, vec2, isClockWise)
     print(theta1, theta2)

     if (theta1<180 and theta2<180):
          return 0
     elif (theta1>180 and theta2>180):
          return 1
     elif (theta1==0 and theta2==0):
          return 3
     else:
          return 2


def read_front_vectors(vec1, vec2):
     if (vec1[1]>0):
          return 0
     elif (vec1[1]<0):
          return 1
     else:
          return 2

def CalAngleBetweenTwoPoints(h, w, isClockWise):
     rotated= [0,0] #h vector will be rotated 90 degree

     if (isClockWise): #h벡터로부터 시계방향 회전 (머리-중심-꼬리 사진)
          rotated[0]= h[1]
          rotated[1]= -h[0]
     else: #h벡터로부터 반시계방향회전 (꼬리-중심-머리 사진)
          rotated[0]= -h[1]
          rotated[1]= h[0]

     hVecsize= math.sqrt(h[0]**2 + h[1]**2)
     wVecsize= math.sqrt(w[0]**2 + w[1]**2)
     
     fAng= math.degrees(math.acos((rotated[0]*w[0] + rotated[1]*w[1]) / (hVecsize * wVecsize)))

     if (fAng>90): #if True, it means the angle between vector h and w is bigger than 180 
          return 360- math.degrees(math.acos((h[0]*w[0] + h[1]*w[1]) / (hVecsize * wVecsize)))
     else:
          return math.degrees(math.acos((h[0]*w[0] + h[1]*w[1]) / (hVecsize * wVecsize)))
     
