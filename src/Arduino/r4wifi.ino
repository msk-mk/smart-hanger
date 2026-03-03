#include <Servo.h>
#include <WiFi.h>
#include "config.h"

const char* ssid = WIFI_SSID;
const char* pass = WIFI_PASS;
const char* serverIP = SERVER_IP;
const int serverport = SERVER_PORT; 

//cloth
const int PULSE_PIN = 2;
const int DIGITAzL_READ_PIN = 3;
const int ANALOG_READ_PIN = 5;

const double E = 5.06; // GPIO電圧実測値
const double R = 2000000; // 2MΩ
const double V = E * 0.632;

WiFiClient client;
Servo myservo;

void setup() {
  Serial.begin(9600);
  delay(10);
  
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  pinMode(PULSE_PIN, OUTPUT);
  digitalWrite(PULSE_PIN, LOW);
  myservo.attach(9);
}

void discharge() {
  pinMode(DIGITAL_READ_PIN, OUTPUT);
  digitalWrite(DIGITAL_READ_PIN, LOW);
  delay(1000);
  pinMode(DIGITAL_READ_PIN, INPUT);
  delay(10);
}

unsigned long charge() {
  digitalWrite(PULSE_PIN, HIGH);
  return micros();
}


void RotateServo(){//モーターを回す
  int pos = 0;

  for (pos = 0; pos <= 180; pos += 1){
    myservo.write(pos);
    delay(15);
  }
  for (pos = 180; pos > 0; pos -= 1){
    myservo.write(pos);
    delay(15);
  }
}


void WaitForResponse(String message){//クライアントからのメッセージを受信
  Serial.print("connecting to ");
  Serial.print(serverIP);
  Serial.print(":");
  Serial.println(serverport);
    
  if (!client.connect(serverIP, serverport)) {
    Serial.println("connection failed");
    return;
  }
  
  client.print(message);

  String m_rcv;
  while(client.connected()){
    if (client.available()){
      m_rcv = client.readStringUntil('\r');
      if(m_rcv == "OK"){
        Serial.println("...OK");
      }else if (m_rcv == "ERROR"){
        Serial.println("...NG");
      }else if(m_rcv == "MOTOR"){
        Serial.println("MOTOR ON");
        RotateServo();
      } else{
        Serial.println("...receiveERROR");
      }
      client.stop();
      break;
    }
  }
  return;
}

void loop() {
  discharge();

  //服側の静電容量
  unsigned long time_start = charge(1);
  double volts = 0;
  while (volts < V){
    volts = double(analogRead(ANALOG_READ_PIN)) / 1023.0 * E;
  }
  double T = micros() - time_start;
  Serial.println(T);
  
  String message = String(loop) + "," + String(T);
  WaitForResponse(message);
  
  digitalWrite(PULSE_PIN, LOW);
  delay(5000);
}
