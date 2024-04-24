#include<Servo.h> // 서보 라이브러리 포함
#include <Wire.h> // 와이어 라이브러리 포함
#define SLAVE 2 // SLAVE 변수를 2로 정의하다.

Servo bottom, foward, height, gripper; // Servo 객체를 생성.
Servo servo[4] = {bottom, foward, height, gripper}; // 4개의 서보 모터를 사용.

int preVal[4] = {70, 85, 90, 120}; // 변수 선언 후 초기 각도 값을 저장.
int pin[4] = {8, 9, 10, 11}; // pin 배열을 선언, 각 서보 모터에 연결된 핀 번호를 저장.

// 각 4개의 제품을 분류할 서보모터의 Servo 객체를 생성.
Servo red;
Servo blue;
Servo green;
Servo yellow;

char ser; // master로부터 받은 명령 저장 변수.
char res; // master에게 보낼 응답 저장 변수.

// 서보 모터의 각도를 저장하는 배열을 선언.
int saveAngle[11][4] = {{70,85,130,120},{70, 116, 130, 120},{70, 125, 130, 120},{77, 125, 130, 120},{77, 125, 130, 65},{77, 117, 130, 65},{150, 117, 130, 65},{150, 117, 80, 65},{150, 117, 80, 120},{150, 85, 80, 120},{70, 85, 90, 120}};
int saveAngle1[11][4] = {{70,85,130,120},{70, 116, 130, 120},{70, 125, 130, 120},{77, 125, 130, 120},{77, 125, 130, 65},{77, 117, 130, 65},{115, 117, 130, 65},{115, 117, 80, 65},{115, 117, 80, 120},{115, 85, 80, 120},{70, 85, 90, 120}};
int saveAngle2[13][4] = {{70,85,130,120},{70, 116, 130, 120},{70, 125, 130, 120},{77, 125, 130, 120},{77, 125, 130, 65},{77, 117, 130, 65},{25, 117, 130, 65},{25, 117, 80, 65},{50, 117, 80, 65},{50, 117, 80, 120},{25, 117, 80, 120},{25, 85, 80, 120},{70, 85, 90, 120}};
int saveAngle3[11][4] = {{70,85,130,120},{70, 116, 130, 120},{70, 125, 130, 120},{77, 125, 130, 120},{77, 125, 130, 65},{77, 117, 130, 65},{15, 117, 130, 65},{15, 117, 80, 65},{15, 117, 80, 120},{15, 85, 80, 120},{70, 85, 90, 120}};

//int btN = 0;

//boolean flag = 0;

void setup() { // 설정 함수. 초기화 및 설정을 수행.
  res = '0'; // 응답 변수 초기화.
  for (int i = 0; i < 4; i++) { // 각 서보 모터에 대해 반복.
    servo[i].attach(pin[i]); // 서보 모터에 핀 연결.
  }
  
  red.attach(2); // 분료 빨간색에 핀 2 연결.
  blue.attach(3); // 분류 파란색에 핀 3 연결.
  green.attach(12); // 분류 초록색에 핀 12 연결.
  yellow.attach(13); // 분류 노란색에 핀 13 연결.
  
  Serial.begin(9600); // 시리얼 통신 시작.

  for (int i = 0; i < 4; i++) { // 각 서보 모터에 대해 반복.
    servo[i].write(preVal[i]); // 초기 각도 설정.
  }
  
  red.write(83); // 분류 빨간색 초기 각도 설정.
  blue.write(82); // 분류 파란색 초기 각도 설정.
  green.write(94); // 분류 초록색 초기 각도 설정.
  yellow.write(97); // 분류 노락색 초기 각도 설정.

  pinMode(6, INPUT_PULLUP); // 핀 6을 풀업 입력 모드로 설정
  pinMode(7, INPUT_PULLUP); // 핀 7을 풀업 입력 모드로 설정

  Wire.begin(SLAVE); // i2c 통신 시작.
  Wire.onReceive(fromMaster); // 마스터로부터 데이터 수신 시 호출할 함수 지정.
  Wire.onRequest(toMaster); // 마스터에게 데이터 요청 시 호출할 함수 지정.
}

void loop() { // 메인 루프 함수. 프로그램이 반복.
  // int Val[4];
  // for (int i = 0; i < 4; i++) {
  //   Val[i] = analogRead(14 + i);

  //   // 조이스틱 반대방향으로 움직이기(arm1, arm2)
  //   if ( i == 2) {
  //     Val[i] = 1024 - Val[i];
  //   }

  //   moveServo(i, Val[i]);
  // }

  // if (digitalRead(6) == 0) {
  //   if (flag == 1) {
  //     btN = 0;
  //     flag = 0;
  //   }
  //   for (int i = 0; i < 4; i++) {
  //     saveAngle[btN][i] = preVal[i];
  //     Serial.println(saveAngle[btN][i]);
  //   }
  //   btN++;
  //   Serial.println("Save Position");
  //   delay(500);
  // }
  

  // if (digitalRead(7) == 0) {
  //   for (int n = 0; n < 1; n++) {
  //     for (int i = 0; i < 4; i++) {
  //       for (int j = 0; j < 4; j++) {
  //         servoMove(j, saveAngle[i][j]);
  //         delay(20);
  //       }
  //       delay(500);
  //     }
  //   }
  //   flag = 1;
  //   Serial.println("Repeat  Position");
  //   delay(1000);
  // }

  // delay(25);
  //}


  int angle; // 각도 변수 선언.

  if (ser != '0'){ // ser 값이 0이 아니라면
    if (ser == 'e'){ // ser 값이 'e'라면
      for (int n = 0; n < 1; n++) { 
        for (int i = 0; i < 11; i++) { // 총 동작수에 따른 로봇 동작.
          for (int j = 0; j < 4; j++) { // bottom, foward, height, gripper 차례대로 실행.
            servoMove(j, saveAngle[i][j]); // servoMove 함수에 매개변수를 2개 준다.
            delay(20);
          }
          delay(500);
        }
      }
      res = 'e';
    }
    if (ser == 'c'){ // ser 값이 'c'라면
      for (int n = 0; n < 1; n++) {
        for (int i = 0; i < 11; i++) {
          for (int j = 0; j < 4; j++) {
            servoMove(j, saveAngle1[i][j]);
            delay(20);
          }
          delay(500);
        }
      }
      res = 'c';
    }
    if (ser == 'i'){ // ser 값이 'i'라면
      for (int n = 0; n < 1; n++) {
        for (int i = 0; i < 13; i++) {
          for (int j = 0; j < 4; j++) {
            servoMove(j, saveAngle2[i][j]);
            delay(20);
          }
          delay(500);
        }
      }
      res = 'i';
    }
    if (ser == 'q'){ // ser 값이 'q'라면
      for (int n = 0; n < 1; n++) {
        for (int i = 0; i < 11; i++) {
          for (int j = 0; j < 4; j++) {
            servoMove(j, saveAngle3[i][j]);
            delay(20);
          }
          delay(500);
        }
      }
      res = 'q';
    }
    if (ser == 'r') { // ser 값이 'r'라면
      for (angle = 83; angle > 30; angle--)
      {
        red.write(angle);
        delay(10);
      }
      res = 'r';
    }
    if (ser == '1') { // ser 값이 '1'라면
      for (angle = 30; angle < 83; angle++)
      {
        red.write(angle);
        delay(10);
      }
      res = '1';
    }
    if (ser == 'b') { // ser 값이 'b'라면
      for (angle = 82; angle > 30; angle--)
      {
        blue.write(angle);
        delay(10);
      }
      res = 'b';
    }
    if (ser == '2') { // ser 값이 '2'라면
      for (angle = 30; angle < 82; angle++)
      {
        blue.write(angle);
        delay(10);
      }
      res = '2';
    }
    if (ser == 'g') { // ser 값이 'g'라면
      for (angle = 94; angle < 150; angle++)
      {
        green.write(angle);
        delay(10);
      }
      res = 'g';
    }
    if (ser == '3') { // ser 값이 '3'라면
      for (angle = 150; angle > 94; angle--)
      {
        green.write(angle);
        delay(10);
      }
      res = '3';
    }
    if (ser == 'y') { // ser 값이 'y'라면
      for (angle = 97; angle < 150; angle++)
      {
        yellow.write(angle);
        delay(10);
      }
      res = 'y';
    }
    if (ser == '4') { // ser 값이 '4'라면
      for (angle = 150; angle > 97; angle--)
      {
        yellow.write(angle);
        delay(10);
      }
      res = '4';
    }    
    //flag = 1;
    delay(1000);
    ser = '0'; // ser 초기화
  }
}


void fromMaster(int bytes){ // 마스터로부터 데이터 받는 함수.
  char ch[bytes]; // 문자열 배열 선언.

  //Serial.println(bytes);
  for(int i=0; i<bytes; i++){ // 수신된 바이트 수만큼 반복
    ch[i] = Wire.read(); // 데이터 읽기
  }
  for(int i=0; i<bytes; i++){ // 수신된 바이트 수만큼 반복
    //Serial.print("read : ");
    Serial.print(ch[i]); // 읽은 데이터 출력
    ser = ch[i]; // ser 변수에 저장
  }
  //ser = ch[0];
  //Serial.println(ser);
  Serial.println(); // 줄 바꿈 출력.
}


void toMaster(){ // 마스터에게 데이터를 보내는 함수.
  if (res != '0'){ // res 값이 0이 아니라면
    Wire.write(res); // 데이터 전송
    Serial.print("send : ");
    Serial.println(res); // 전송한 데이터 출력
    res = '0'; // res 초기화
  }
}

// int isAction = 0;

// if(isAction){
//   Wire.requestFrom(SLAVE,1);
//   char c=Wire.read();
//   Serial.println(c);
//   isAction = 0;

// }


// void moveServo(byte num, int joy) {
//   if (joy > 900) {
//     preVal[num] += 1;
//     if (num == 0) {
//       if (preVal[num] > 160) {
//         preVal[num] = 160;
//       }
//     }
//     else if (num == 1) {
//       if (preVal[num] > 150) {
//         preVal[num] = 150;
//       }
//     }
//     else if (num == 2) {
//       if (preVal[num] > 180) {
//         preVal[num] = 180;
//       }
//     }
//     else if (num == 3) {
//       if (preVal[num] > 140) {
//         preVal[num] = 140;
//       }
//     }
//   }

//   else if (joy < 200) {
//     preVal[num] -= 1;
//     if (num == 0) {
//       if (preVal[num] < 20) {
//         preVal[num] = 20;
//       }
//     }
//     else if (num == 1) {
//       if (preVal[num] < 40) {
//         preVal[num] = 40;
//       }
//     }
//     else if (num == 2) {
//       if (preVal[num] < 30) {
//         preVal[num] = 30;
//       }
//     }
//     else if (num == 3) {
//       if (preVal[num] <= 90) {
//         preVal[num] = 90;
//       }
//     }
//   }

//   servo[num].write(preVal[num]);
// }



void servoMove(int num, int angle) { // 서보 모터를 움직이는 함수. 지정된 각도로 서보 모터를 움직인다.
  if (preVal[num] > angle) { // 현재 각도가 목표 각도보다 크다면
    for (int i = preVal[num] ; i > angle; i--) { // 현재 각도부터 목표 각도까지 반복
      servo[num].write(i); // 서보 모터 제어
      delay(20);
    }

    preVal[num] = angle; // 현재 각도 갱신
  }

  if (preVal[num] < angle) { // 현재 각도가 목표 각도보다 작다면
    for (int i = preVal[num] ; i < angle; i++) { // 현재 각도부터 목표 각도까지 반복
      servo[num].write(i); // 서보 모터 제어
      delay(20);
    }

    preVal[num] = angle; // 현재 각도 갱신
  }
}
