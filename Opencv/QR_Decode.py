import cv2
from pyzbar.pyzbar import decode
from datetime import datetime

def decode_qr_from_stream():
    # 웹캠 시작
    cap = cv2.VideoCapture(1)

    # 웹캠 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # 웹캠에서 프레임 읽기
        ret, frame = cap.read()

        if not ret:
            break
        
        # 프레임을 어둡게 만들어서 QR 코드를 더 잘 감지할 수 있도록 함
        dark_frame = cv2.convertScaleAbs(frame, alpha=0.1, beta=1)

        # 프레임에서 QR 코드 디코드
        decoded_objects = decode(dark_frame)

        for obj in decoded_objects:
            # 현재 시간을 타임스탬프로 가져오기
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # QR 코드 데이터와 타임스탬프 출력
            print(f"Timestamp: {timestamp}, Data: {obj.data.decode('utf-8')}")

            # QR 코드 주변에 사각형 그리기 (선택 사항)
            cv2.rectangle(frame, (obj.rect.left, obj.rect.top), 
                          (obj.rect.width + obj.rect.left, obj.rect.height + obj.rect.top), 
                          (255, 0, 0), 2)

        # 프레임 표시
        cv2.imshow('Webcam', frame)

        # 'q'를 눌러서 루프 탈출
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 리소스 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    decode_qr_from_stream()