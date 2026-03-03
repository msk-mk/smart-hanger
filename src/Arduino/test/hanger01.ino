#include <WiFi.h>
#include <HttpClient.h>
#include "../config.h"

const int PULSE_PIN = 2;
const int DIGITAL_READ_PIN = 3;
const int ANALOG_READ_PIN = 5;

const char *ssid = WIFI_SSID;
const char *password = WIFI_PASS;
const String token = LINE_NOTIFY_TOKEN;

const double E = 5.06; // GPIO電圧実測値
const double R = 2000000; // 2MΩ
const double V = E * 0.632;

void setup()
{
  WiFi.begin(ssid, password);
  Serial.begin(115200);
  Serial.print("Connecting...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected to Wi-Fi");
  
  pinMode(PULSE_PIN, OUTPUT);
  digitalWrite(PULSE_PIN, LOW);
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

void loop() {
  discharge();

  unsigned long time_start = charge();

  double volts = 0;
  while (volts < V)
  {
    volts = double(analogRead(ANALOG_READ_PIN)) / 1023.0 * E;
  }

  double T = micros() - time_start;

  double c;
  char *farad = "pF";

  c = T / R * 1000000; // pF
  farad = "pF";
  
  Serial.print(c);
  Serial.print(farad);

  if (c > 200){
    sendMessage("LINE Notify");
  }

  Serial.println();
  digitalWrite(PULSE_PIN, LOW);
}

void sendMessage(String message) { 
  HttpClient http;
  WiFiClient client;

  String url = "https://notify-api.line.me/api/notify";
  http.begin(client, url);
  http.sendHeader("Content-Type", "application/x-www-form-urlencoded");
  http.sendHeader("Authorization", "Bearer " + token);

  String query = "message=" + message;
  http.POST(query);

  String body = http.readString();
  Serial.println("Sent the message");
  Serial.println(body);
  http.end();
}
