#include <Servo.h>

Servo myservo;  //サーボオブジェクトの生成

int pos = 0;    //角度を指定する変数

void setup() {
  myservo.attach(9);      //myservoとサーボモーターの対応付け
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1){
    myservo.write(pos);
    delay(15);
  }
  for (pos = 180; pos > 0; pos -= 1){
    myservo.write(pos);
    delay(15);
  }
}
