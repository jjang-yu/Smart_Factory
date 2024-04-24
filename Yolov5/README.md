# YOLOV5 환경 설정

일반 리눅스 환경에서는 버전이 조금이라도 맞지 않으면 충돌이 일어나 패키지 버전을 맞추기 위해 venv 표준 라이브러리 가상환경 생성
- Python (3.9.2 .ver)
- Opencv (4.9.0 .ver)
- TensorFlow (2.16.1 .ver)

# YOLOV5 설치 명령어 

```
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

# 라벨링 및 데이터 학습 후 실행

- Roboflow에서 이미지와 색상을 각각 라벨링
- <img src="https://github.com/jjang-yu/Smart_Factory/assets/160578079/bd260f54-e4a6-4b88-a688-e17e5ed95c51" widht="150" height="150"/>
- 데이터 학습 -> 이미지 크기 : 320, 배치 사이즈 : 16, 에포크 횟수 : 200, 모델 크기 : s
  ```
  python train.py --img 320 --batch 16 --epochs 200 --data data.yaml --cfg yolov5s.yaml --weights yolov5s.pt
  ```
  #### detect.py 파일 최적화 및 실행

  - 학습 시킨 모델을 실행하려면 detect.py를 기존 코드의 weights, source, data 루트를 학습 모델로 변경
  - Raspberry Pi의 성능이 좋지 않아 실시간 인식의 속도가 느림
  - 프레임과 해상도를 인식 가능할 정도의 최소 값으로 조정
  - Raspberry Pi의 그래픽 메모리를 256MB로 설정 (512MB로 설정하면 태초마을로 돌아가니 조심하세요^^..)
  - 터미널에서 detect.py 실행 ⬇ 실행 명령어
    ```
    # weight : 가중치 파일, source : 인덱스 1번째의 카메라, data : 학습 시킨 .yaml 파일
    python3 detect.py --weight dataset/best.pt --source 1 --img 320 --data dataset/data.yaml
    ```
