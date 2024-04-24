# Opencv 환경 설정

- 일반 리눅스 환경에서는 버전이 조금이라도 맞지 않으면 충돌이 일어나 패키지 버전을 맞추기 위해 venv 표준 라이브러리 가상환경 생성
- Python (3.9.2 .ver)
- Opencv (4.9.0 .ver)
- TensorFlow (2.16.1 .ver)

# 패키지 설치 명령어

```
sudo apt-get update
sudo apt-get install python3-venv
python3 -m venv opencv-venv
source opencv-venv/bin/activate

pip install --upgrade pip
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


sudo apt-get install build-essential cmake pkg-config -y
sudo apt-get install libjpeg-dev libtiff5-dev libpng-dev -y
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev -y
sudo apt-get install libxvidcore-dev libx264-dev -y
sudo apt-get install libfontconfig1-dev libcairo2-dev -y
sudo apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev -y
sudo apt-get install libgtk2.0-dev libgtk-3-dev -y
sudo apt-get install libatlas-base-dev gfortran -y
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103 -y
sudo apt-get install libopenblas-base -y
sudo apt-get install python3-pyqt5 -y
sudo apt-get install python3-dev -y

pip install numpy
pip install opencv-python

pip install tensorflow==2.16.1
```
#### Shape.py와 QR_Decode.py 파일 실행

- ⬇Shape.py 실행

  <img src="https://github.com/jjang-yu/Smart_Factory/assets/160578079/b10f6338-8e8f-44dc-871e-ea057844151b" wedht="150" height="150"/>

- ⬇QR_Decode.py 실행

  <img src="https://github.com/jjang-yu/Smart_Factory/assets/160578079/b49490b0-4165-40ad-8f54-ff5ce42ed103" wedht="150" height="150"/>

