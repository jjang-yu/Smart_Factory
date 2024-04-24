// 라이브러리
// currentPosition() //현재 위치 값
// move(distance)  //이동할 거리 지정
// stepper.setCurrentPosition(position); //현재 스탭을 설정
// stepper.currentPosition(); //현재 스탭을 반환
// stepper.setAcceleration(2000); //가속량을 설정함
// stepper.moveTo(1000); //목표스탭량을 설정함
// stepper.runToPosition(); //가속도 조절 스탭모터제어

#include <AccelStepper.h> //스텝모터
#include <Wire.h> // I2C통신
#include <SoftwareSerial.h> // UART통신


#define moterInterfaceType 1 // 스텝모터의 인터페이스 타입을 나타내는 상수
#define SLAVE 2 // 슬레이브
#define sensor_cam 3 // 적외선센서
#define sensor_robot 4 // 적외선센서
#define enablePin 5 // 스텝모터(전원해제핀)
#define dirxPin 6 // 스텝모터
#define stepxPin 7 // 스텝모터
#define RX_PIN 8 // Rx
#define TX_PIN 9 // Tx
#define switch_R 10 // 마이크로스위치A
#define switch_G 11 // 마이크로스위치B
#define switch_B 12 // 마이크로스위치C
#define switch_Y 13 // 마이크로스위치D

#define lamp_R A1 // 램프 Red
#define lamp_Y A2 // 램프 Yellow
#define lamp_G A3 // 램프 Green



AccelStepper stepperx = AccelStepper(moterInterfaceType, stepxPin, dirxPin);
// AccelStepper stepperx = AcclStepper(연결방식, step핀, dir핀)

int motorSpeed = 600;

int state1 = 1; // 센서 상태 저장 변수
int state2 = 1; // 센서 상태 저장 변수
int isStop = 1; // 스텝모터 중지 결정 변수

int count_R = 0; // 마이크로스위치
int count_G = 0; // 마이크로스위치
int count_B = 0; // 마이크로스위치
int count_Y = 0; // 마이크로스위치

int cam;
int robot;

//byte count = 0;

int isAction = 0;
char action_value = '\0';

SoftwareSerial uartSerial(8, 9); // RX, TX UART통신----------------------------------------------!!
String inputString = "";
boolean stringComplete = false;

void setup() {   
  Serial.begin(9600);
  Serial.println("NSF START");
  pinMode(enablePin, OUTPUT); // 모터는 OUTPUT
  digitalWrite(enablePin, LOW); 

  stepperx.setCurrentPosition(0);
  stepperx.setSpeed(motorSpeed);
  stepperx.setMaxSpeed(1000); // 최대속도

  pinMode(sensor_cam, INPUT); // 센서는 INPUT
  pinMode(sensor_robot, INPUT);
  pinMode(switch_R, INPUT);
  pinMode(switch_G, INPUT);
  pinMode(switch_B, INPUT);
  pinMode(switch_Y, INPUT);

  pinMode(lamp_R, OUTPUT);
  pinMode(lamp_Y, OUTPUT);
  pinMode(lamp_G, OUTPUT);

  digitalWrite(lamp_R, HIGH);
  digitalWrite(lamp_Y, HIGH);
  digitalWrite(lamp_G, HIGH);

  Wire.begin(); // 마스터 
  uartSerial.begin(9600); //uartSerial 통신
}

unsigned long sensorDisabledUntil = 0;
unsigned long sensorDisabledUntil2 = 0;
void loop() {

  state1 = digitalRead(sensor_cam); // 적외선 센서를 읽어와 저장  
  state2 = digitalRead(sensor_robot);
  
  if (state1 == LOW) {
    if (millis() > sensorDisabledUntil) {
      // Serial.println(state1);
      sensorDisabledUntil = millis();
    }
    else {
      state1 = HIGH;
    }
  }
  if (state2 == LOW) {
    if (millis() > sensorDisabledUntil2) {
      // Serial.println(state2);
      sensorDisabledUntil2 = millis() + 10000;
    }
    else {
      state2 = HIGH;
    }
  }

  if (!isStop) // 센서가 멈추지 않을 경우
  {    
    if (state1 == LOW) { //센서가 감지되면 
      isStop = 1; // 동작을 멈춤
      Serial.print("sensor1=");
      uartSerial.println("sensorCam");
    }
    else if (state2 == LOW){
      isStop = 1; // 동작을 멈춤
      Serial.print("sensor2=");
      uartSerial.println("sensorRobot");
    }
    else { // 센서가 감지되지 않으면
      stepperx.setSpeed(motorSpeed); // 설정된 속도와 방향
      stepperx.runSpeed(); // 스텝 모터를 움직임
      isStop = 0; 
    }  
  }   

  if (uartSerial.available() > 0) {
    serialEvent();
  }

  if (stringComplete) {
    Serial.print("stringComplete: ");
    Serial.println(inputString);

    if (inputString.startsWith("forceStart")) {
      Serial.println("forceStart");
      isStop = 0;
      sensorDisabledUntil = millis() + 2000;
      // inputString.replace("forceStart:", "");

      if (inputString.indexOf(":R") > -1) {
        inputString = "servoR:on";
      }
      else if (inputString.indexOf(":G") > -1) {
        inputString = "servoG:on";
      }
      else if (inputString.indexOf(":B") > -1) {
        inputString = "servoB:on";
      }
      else if (inputString.indexOf(":Y") > -1) {
        inputString = "servoY:on";
      }
      else {
        inputString = "sensorStart";
      }      
    }

    if (inputString.startsWith("lamp")) {
      if (inputString.indexOf("On") > -1) {
        setLampOnAll();
      }
      if (inputString.indexOf("Off") > -1) {
        setLampOffAll();
      }
    }

    if (inputString.startsWith("sensor")) {
      if (inputString.indexOf("start") > -1) {
        isStop = 0;
      }
    }

    if (inputString.startsWith("convayor")) {
      if (inputString.indexOf("Start") > -1) {
        isStop = 0;
        setLampOnGreen();
      }
      if (inputString.indexOf("Stop") > -1) {
        isStop = 1;
        setLampOnYellow();
      }
      if (inputString.indexOf("Finish") > -1) {
        isStop = 1;
        setLampOffAll();
      }

      stringComplete = false;
      inputString = "";
      return;
    }

    Wire.beginTransmission(SLAVE); // SLAVE에게 전송
    Serial.print("inputString=");
    Serial.println(inputString);
    if (inputString.startsWith("servoR")) {
      if(inputString.indexOf("on") > -1){ // Red_Servo OPEN
        Wire.write('r');
        action_value = 'r';
      }                                                                
      if(inputString.indexOf("off") > -1){ // Red_Servo CLOSE
        Wire.write('1');
        action_value = '1';
      }
    }
    if (inputString.startsWith("servoB")) {
      if(inputString.indexOf("on") > -1){ // Blue_Servo OPEN
        Wire.write('b');
        action_value = 'b';
      }                                                                
      if(inputString.indexOf("off") > -1){ // Blue_Servo CLOSE
        Wire.write('2');
        action_value = '2';
      }
    }
    if (inputString.startsWith("servoG")) {
      if(inputString.indexOf("on") > -1){ // Green_Servo OPEN
        Wire.write('g');
        action_value = 'g';
      }                                                                
      if(inputString.indexOf("off") > -1){ // Green_Servo CLOSE
        Wire.write('3');
        action_value = '3';
      }
    }
    if (inputString.startsWith("servoY")) {
      if(inputString.indexOf("on") > -1){ // Yellow_Servo OPEN
        Wire.write('y');
        action_value = 'y';
      }                                                                
      if(inputString.indexOf("off") > -1){ // Yellow_Servo CLOSE
        Wire.write('4');
        action_value = '4';
      }
    }
    if (inputString.startsWith("robotE")) {
      Wire.write('e');
      action_value = 'e';
      setLampOnRed();
    }
    if (inputString.startsWith("robotC")) {
      Wire.write('c');
      action_value = 'c';
      setLampOnRed();
    }
    if (inputString.startsWith("robotI")) {
      Wire.write('i');
      action_value = 'i';
      setLampOnRed();
    }
    if (inputString.startsWith("robotQ")) {
      Wire.write('q');
      action_value = 'q';
      setLampOnRed();
    }
    Wire.endTransmission();
    isAction = 1;

    stringComplete = false;
    inputString = "";
  } 
 

  if (isAction) {
    Wire.requestFrom(SLAVE,1); // 1바이트씩 받기
    char se=Wire.read();

    if (se == action_value) {
      Serial.print("wire read, read char, action : ");
      Serial.print(se);
      Serial.print(",");
      Serial.print(int(se));
      Serial.print(",");
      Serial.println(action_value);

      isAction = 0;

      if (se == 'r') {
        uartSerial.println("servoR");
        delay(500);
        return;
      }
      if (se == 'g') {
        uartSerial.println("servoG");
        delay(500);
        return;
      }
      if (se == 'b') {
        uartSerial.println("servoB");
        delay(500);
        return;
      }
      if (se == 'y') {
        uartSerial.println("servoY");
        delay(500);
        return;
      }
      if (se == 'e' || se == 'c' || se == 'i' || se == 'q') {
        // setLampOnGreen();
        uartSerial.println("restart");
        delay(500);
        return;
      }

      action_value = "";
    }
  }

  if (digitalRead(switch_R) == HIGH) {
    count_R++;
    Serial.print("switch_R :");
    Serial.println(count_R);

    uartSerial.println("switchR");
    delay(500);
    return;
  }  
  if (digitalRead(switch_G) == HIGH) {
    count_G++;
    Serial.print("switch_G :");
    Serial.println(count_G);

    uartSerial.println("switchG");
    delay(500);
    return;
  }
  if (digitalRead(switch_B) == HIGH) {
    count_B++;
    Serial.print("switch_B :");
    Serial.println(count_B);

    uartSerial.println("switchB");
    delay(500);
    return;
  }
  if (digitalRead(switch_Y) == HIGH) {
    count_Y++;
    Serial.print("switch_Y :");
    Serial.println(count_Y);

    uartSerial.println("switchY");
    delay(500);
    return;
  }
}

void serialEvent() {
  while (uartSerial.available()) {
    char inChar = (char)uartSerial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void setLampOnRed() {
  setLampOffAll();
  digitalWrite(lamp_R, LOW);
}

void setLampOnYellow() {
  setLampOffAll();
  digitalWrite(lamp_Y, LOW);
}

void setLampOnGreen() {
  setLampOffAll();
  digitalWrite(lamp_G, LOW);
}

void setLampOnAll() {
  digitalWrite(lamp_R, LOW);
  digitalWrite(lamp_Y, LOW);
  digitalWrite(lamp_G, LOW);
}

void setLampOffAll() {
  digitalWrite(lamp_R, HIGH);
  digitalWrite(lamp_Y, HIGH);
  digitalWrite(lamp_G, HIGH);
}
