import constant as constant
import cv2
import numpy as np
import PoseDetermining as pd

poses = []
top = 1  # poses 배열 index
Pj = 1
P_MAX = constant.Probability[0][2]*constant.Probability[2][0]*constant.Probability[0][2]*constant.Probability[2][0]

while True:
    new_pose = pd.read_vectors()    ##############들어오는 숫자
    constant.frame_cnt += 1  # cnt 증가
    if (constant.frame_cnt > constant.frame_limit) and (top != 4):  # 배열 다 안 찼는데 frame 개수 초과
        print("not","bird!")
        constant.frame_cnt = 0
        top = 1
        Pj = 1  # 초기화
    if top == 1:  # 배열이 비어있으면
        poses.append(new_pose)  # 넣고
        top += 1  # 배열 index 증가
        Pj *= constant.Probability[new_pose][new_pose]  # 확률계산
        old_pose = new_pose  # 비교용 갱신
    elif top == 4:  # 배열 꽉 참
        Pj /= P_MAX
        if Pj >= constant.threshold:
            print("bird")
        else:
            print("not"," ","bird!")
        constant.frame_cnt = 0
        top = 1
        Pj = 1  # 초기화
    else:  # 배열에 뭐 있으면 전 거랑 pose 숫자가 같은지 다른지 비교 
        if old_pose == new_pose: continue;  #같으면 pass
        else:  # 다르면 넣고 확률 계산
            poses.append(new_pose)  # 넣고
            top += 1  # 배열 index 증가
            Pj *= constant.Probability[old_pose][new_pose]  # 확률계산
            old_pose = new_pose  # 비교용 갱신							  
    
