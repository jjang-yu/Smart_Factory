#컨베이어 벨트 위에서 빛 반사로 인해 도형들이 잘 잡히지 않아서 명도와 대비값을 낮추었고, 각 색상의 RGB 값을 HSV 값으로 변환하여 추출해주었다.
#그리고 도형의 검출 면적과 메시지 출력도 특정 면적 값이 검출이 되어야 출력이 되도록 변경했다. 

import cv2
import numpy as np
import math
from datetime import datetime

total_fps = 0.0  # 전체 프레임 속도의 합을 저장할 변수
average_fps = 0.0  # 평균 프레임 속도를 저장할 변수
cnt = 1  # 프레임 수를 카운트할 변수

# 웹캠으로부터 영상을 캡처
capture = cv2.VideoCapture(1)

# 영상의 너비를 설정
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

# 영상의 높이를 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 영상의 초당 프레임 수를 설정
capture.set(cv2.CAP_PROP_FPS, 65)

# 사각형과 원이 각각 감지되었는지 여부를 나타내는 변수들
rac_detected = False
cir_detected = False

# 현재 시간을 가져와서 문자열로 변환하여 저장
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 무한 루프
while True:
    start_time = cv2.getTickCount()  # 현재 시간을 가져와서 시작 시간으로 설정
    ret, img = capture.read()  # 웹캠에서 영상 프레임을 읽음

    if not ret:  # 만약 프레임을 제대로 읽지 못했다면 루프를 종료
        break

    # 이미지를 HSV 색 공간으로 변환
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 빨간색, 노란색, 초록색, 파란색, 주황색의 색상 범위 설정
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])

    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([30, 255, 255])

    lower_green = np.array([35, 40, 0])
    upper_green = np.array([85, 255, 255])

    lower_blue = np.array([90, 100, 100])
    upper_blue = np.array([130, 255, 255])

    lower_orange = np.array([0, 50, 50])
    upper_orange = np.array([30, 255, 255])

    # 각 색상에 대한 마스크 생성
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # 각 마스크를 합치기
    mask = mask_green | mask_red | mask_yellow | mask_blue | mask_orange

    # 마스크를 이미지에 적용하여 색상을 검출
    masked_image = cv2.bitwise_and(img, img, mask=mask)

    # 어두운 프레임 생성
    dark_frame = cv2.convertScaleAbs(masked_image, alpha=0.8, beta=2)

    # 이미지 가장자리 감지
    edge_img = cv2.Canny(img, 50, 200)

    # 윤곽선 찾기
    contours, _ = cv2.findContours(edge_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, cv2.arcLength(contour, True) * 0.02, True)

        # 추출할 사각형의 면적 조정
        if len(approx) == 4 and 20000 < abs(cv2.contourArea(approx)) > 23500 and cv2.isContourConvex(approx):
            for i in range(4):
                cv2.circle(img, tuple(approx[i][0]), 3, (255, 0, 0), 3)

            for i in range(4):
                cv2.line(img, tuple(approx[i][0]), tuple(approx[(i + 1) % 4][0]), (0, 0, 255), 2)

            cv2.imwrite('/home/nsf/사진/rectangle.jpg', img) # 이미지 저장

            rac_detected = True # 사각형이 감지됨을 나타내는 변수를 True로 설정
            print('외형 오류 없음')
            break # 사각형이 감지되면 루프를 빠져나감

    circles = cv2.HoughCircles(
        edge_img, cv2.HOUGH_GRADIENT, dp=1, minDist=100, param1=200, param2=25, minRadius=80, maxRadius=98) # 추출할 원형의 면적 조정

    if circles is not None and len(circles) > 0:
        circles = np.round(circles[0, :]).astype("int") # 검출된 원의 정보를 가져와서 반올림 후 정수형으로 변환

        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 3)

        for circle in circles:
            area = np.pi * circle[2] * circle[2]
            # 오류 메시지를 출력할 원형의 면적 조정
            if 29000 < area < 30000:
                cir_detected = True
                print('외형 오류!')

    cv2.imshow("PreviewImage", img) # 원본 이미지 표시
    cv2.imshow("Edge", edge_img) # 엣지 이미지 표시

    key = cv2.waitKey(1) #사용자 입력을 대기

    if key > 10: # 사용자가 키를 누르면 루프 종료
        break

    if rac_detected: # 사각형이 감지되었다면 루프 계속 실행
        continue
    
    end_time = cv2.getTickCount() # 현재 시간을 가져와서 종료 시간 설정
    elapsed_time = (end_time - start_time) / cv2.getTickFrequency() # 경과 시간 계산
    fps = 1.0 / elapsed_time # 프레임 속도 계산

    total_fps += fps # 전체 프레임 속도에 현재 프레임 속도를 더함
    average_fps = total_fps / cnt # 평균 프레임 속도 계산
    cnt += 1

    # 프레임 수가 100이 되면 초기화
    if cnt == 100:
        cnt = 1
        total_fps = 0.0
    # 경과 시간과 현재 프레임 속도, 평균 프레임 속도 출력
    print(f"Elapsed T = {elapsed_time * 1000:.3f} ms, Frame = {fps:.3f} (fps), Avrg Frame Rate = {average_fps:.3f}")

capture.release()
cv2.destroyAllWindows()