# Smart_Factory_Project
#### 팀원
강시은: [Github](https://github.com/sieun-20)

백승기: [Github](https://github.com/seunggi-baek)

장유정: [Github](https://github.com/jjang-yu)

김희철

# 프로젝트 설명
객체인식 기술을 활용하여 물체 감지 시스템을 구축하고 해당 물체를 분류하는 서비스.

### 사용 부품

Raspberry pi4 B+, Arduino, LCD, PiCamera V2, WebCam(APC480)

### 사용 언어

C, C++, Python

### 사용 서비스

Raspberry Pi OS (Legacy, 64-bit), YOLOv5, OpenCV, PyTorch, Arduino IDE, MariaDB, Workbench, Database, Flask

### 분류 항목
1. 이미지 분류(Yolov5)
2. 색상 분류 (Yolov5)
3. 외형 분류(Opencv)
4. QRcode 인식(Opencv)

# 프로젝트 설명

### 작동 원리

>1) 웹사이트 접속
>
>2) Raspberry Pi(server) 부팅
>   -부팅 시 Flask 서버 자동 실행
>   #자동실행 방법
>   - sudo vim /etc/xdg/lxsession/LXDE-pi/autostart
>   ``` Python
>   #Flask app.py 실행
>   @lxterminal -e python /var/www/nsfweb/app.py
>   
>   #브라우저 실행
>   chromium-browser --start--maxximized --kiosk
>   192.168.1.193:5000
>   ```
>4) HMI 화면 선택
>- 관리자, 사용자 모드 선택 가능
>- 
>- 관리자 모드
>-  각 서보모터, 스위치, 컨베이어 작동 테스트 가능
>-  
>- 사용자 모드
>-  1) 목표 수량 입력 후 시작 버튼 클릭
>-  2) 데이터 베이스 테이블에 하나의 행 추가
>-  3) 컨베이어 벨트 가동 및 타워램프 초록불 ON
>
>5) 객체 및 QRcode 분석
>- 1) 제품이 적외선 센서에 감지되면 컨베이어 벨트 가동 중지
>- 2) PiCamera를 통해 외형 및 QRcode 리딩, 서버에서 QR_Shape.sh 파일 실행 후 QR_Shape.py를 실행하여 도출 결과값 서버로 전송
>- 3) 서버에서 Detect.sh 파일 실행 후 Detect.py 파일 실행하여 WebCam을 통해 이미지 및 색상 감지가 되면 도출 결과값 1초마다 서버로 전송 
>-  3-1) Detect.py 실행 명령어
>     ```
>     python3 detect.py --weight dataset/best.pt --source 1 --img 320 --data dataset/data.yaml
>     ```
>- 4)  결과값을 전부 받으면 컨베이어 벨트 재가동
>- 5)  각 구역으로 분류
>- 6)  분류 시 스위치 센서를 통해 제품 카운트 업데이트
>- 7)  오류 발생 시 오류 카운트 업데이트
>- 8)  오류 제품은 로봇팔이 있는 지점으로 이동
>- 9)  적외선 센서 감지되면 컨베이어 벨트 가동 중지
>- 10)  로봇팔을 통한 오류 제품 분류
>- 11)  목표 수량 도달 완료 시 가동 종료

### 실제

#### 외부
<img src="https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/e8302163-633d-450a-a181-717406558e0f" width="400" height="300"/>

<img src="https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/4e0582db-38ff-4386-9e0a-c942ce7aba64" width="200" height="300"/>

1-1) 파이캠
1-2) 웹캠
2)  제품 분류 서보모터 
3)  컨베이어 스텝모터  
4)  적외선 센서  
5)  로봇팔 서보모터
6)  제품 카운트 스위치 
7)  타워램프 
8)  HMI Display

#### 기계실 내부

<img src="https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/9b8e01d2-1204-41c9-aa5e-d68f1db3a99a" width="400" height="300"/>

<img src="https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/8bcb6b7f-eef4-4945-bfee-aee8cc53a714" width="200" height="300"/>

<img src="https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/dd2a24d1-e731-4748-9acf-7bc5fefc9eb4" width="150" height="300"/>

1) 타워램프 외부 전압 12V
2) 컨베이어 스텝모터 드라이버 & 외부 전압 12V
3) 라즈베리파이 (서버)
4) 아두이노 (마스터) & PCB 기판
5) 라즈베리파이 (객체 감지)
6) HMI Display
7) 아두이노 (슬레이브) & 쉴드


#### 객체인식
![객체 인식](https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/888c4f6e-4acb-495d-b9d8-2b20849d4802)

### 회로도
<img src="https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/f1233be5-0b6b-4e00-8388-fda183c82527" width="800" height="600"/>

### PCB 회로도
<img src="https://github.com/jjang-yu/Smart_Factory_Project/assets/160578079/44bd04c6-526e-4c09-9fe1-fbf386b0a033" width="600" height="400"/>
