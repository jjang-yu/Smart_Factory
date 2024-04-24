import cv2
import numpy as np
import math
from pyzbar.pyzbar import decode
from datetime import datetime 
import time

class QRcode:
    def qr_decode(self,frame):
        # 프레임을 어둡게 만들어서 QR 코드를 더 잘 감지할 수 있도록 함
        dark_frame = cv2.convertScaleAbs(frame, alpha=0.1, beta=0)

        QR = {}

        # QR 코드를 프레임에서 디코딩
        decoded_objects = decode(dark_frame)

        for obj in decoded_objects:

            # QR 코드 데이터를 딕셔너리에 저장
            QR = {"QR" : obj.data.decode('utf-8')}
           
           # QR 코드에 사각형을 그림
            cv2.rectangle(frame, (obj.rect.left, obj.rect.top), 
                          (obj.rect.width + obj.rect.left, obj.rect.height + obj.rect.top), 
                          (255, 0, 0), 2)

            return QR

class Shapes:
    def shapes_decode(self,img):


        rec_detected = "" 

        # 이미지를 HSV로 변환
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 빨간색, 노란색, 초록색, 파란색의 색상 범위 설정
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([180, 255, 255])

        lower_yellow = np.array([15, 50, 50])
        upper_yellow = np.array([30, 255, 255])

        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])

        lower_blue = np.array([90, 100, 100])
        upper_blue = np.array([130, 255, 255])

        lower_orange = np.array([0,50,50])
        upper_orange = np.array([30,255,255])

        # 각 색상에 대한 마스크 생성
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

        # 각 마스크를 합치기
        mask =  mask_green | mask_red | mask_yellow | mask_blue | mask_orange

        # 마스크를 이미지에 적용하여 색상을 검출
        masked_image = cv2.bitwise_and(img, img, mask=mask)

        dark_frame = cv2.convertScaleAbs(masked_image, alpha=0.8, beta=2)
        edge_img = cv2.Canny(dark_frame, 100, 200)

        # 윤곽선을 찿음
        contours, _ = cv2.findContours(edge_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
       

        for contour in contours:
            # 다각형 근사화
            approx = cv2.approxPolyDP(contour, cv2.arcLength(contour, True) * 0.02, True)
            # 특정 크기의 사각형을 검출
            if len(approx) == 4 and 23500 < abs(cv2.contourArea(approx)) > 23800: #and cv2.isContourConvex(approx):
                # 사각형의 윤곽선과 꼭지점을 그림
                for i in range(4):
                    cv2.circle(img, tuple(approx[i][0]), 3, (255, 0, 0), 3)

                for i in range(4):
                    cv2.line(img, tuple(approx[i][0]), tuple(approx[(i + 1) % 4][0]), (0, 0, 255), 2)                

                # 사각형이 검출되면 결과를 "rectangle"로 저장 
                rec_detected = "rectangle"
                break

            

        circles = cv2.HoughCircles(
            # 원 검출
            edge_img, cv2.HOUGH_GRADIENT, dp=1, minDist=100, param1=200, param2=25, minRadius=60, maxRadius=90)    

        if circles is not None and len(circles) > 0:
            circles = np.round(circles[0, :]).astype("int")

            # 검출된 원에 윤곽선을 그림
            for (x, y, r) in circles:
                cv2.circle(img, (x, y), r, (0, 255, 0), 3)
            
            # 각 면적을 계산하고, 특정 범위 내의 원을 검출
            for circle in circles:
                area = np.pi * circle[2] * circle[2]
                #print(area)
                if 13100 < area < 14800:
                    # 원이 검출되면 결과를 "circle"로 저장
                    rec_detected = "circle"
                    break

        # 결과 값이 조건문과 맞으면 shape_result 값 리턴
        shape_result = {}
        if rec_detected == "rectangle":
            shape_result["Shape"] = "Success"
        elif rec_detected == "circle":
            shape_result["Shape"] = "Error"
        else:
            # 외형을 검출하지 못하면 "Failed" 값 리턴
            shape_result["Shape"] = "Failed"

        return shape_result



if __name__ == "__main__":
    # QR 코드와 외형을 디코딩하기 위한 객체 생성
    qr = QRcode()
    shape = Shapes()
       
    # 0번 인덱스의 카메라를 불러와서 해상도와 프레임 값 조정
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # 초기 QR 코드와 외형 결과를 None으로 설정
    QR = None
    shape_result = None


    # count = 0
    # 10번의 프레임을 처리하여 QR 코드와 외형을 검출
    for count in range(10):
        ret, frame = cap.read()
        if not ret:
            print("캡쳐 오류")
            continue

        # QR 코드 디코딩
        QR = qr.qr_decode(frame)

        #print(f"count: {count}")
        # 외형 디코딩
        shape_result = shape.shapes_decode(frame)

        # 외형이 성공적으로 인식되었을 경우 반복문 종료
        if shape_result["Shape"] != "Failed":
            break
        # 0.2초 대기 후 다음 프레임 처리
        time.sleep(0.2)

    # QR 코드와 외형 결과 값 조합하여 최종 결과 생성
    if QR is not None and shape_result is not None:
        combined_result = {**QR, **shape_result}
        #print(combined_result)
    elif shape_result["Shape"] == "Error":
        QR = {"QR": ""}
        combined_result = {**QR, **shape_result}
        #print(combined_result)
    else:
        QR = {"QR": ""}
        shape_result["Shape"] = "Failed"
        combined_result = {**QR, **shape_result}
        #print(combined_result)

    # 최종 결과 값 출력
    print(combined_result)


