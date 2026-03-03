#include <WiFi.h>
#include "../config.h"

const char* ssid = WIFI_SSID;
const char* pass = WIFI_PASS;
const char* serverIP = SERVER_IP;
const int serverport = SERVER_PORT; 

void setup() {
  Serial.begin(115200);
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
}

void loop() {
  delay(3000);
  Serial.print("connecting to ");
  Serial.print(serverIP);
  Serial.print(":");
  Serial.println(serverport);
  
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
    
  if (!client.connect(serverIP, serverport)) {
    Serial.println("connection failed");
    return;
  }
  while(true){
    client.print("Hello!");
    delay(1000);
    if(!client.connected()){
      client.stop();
      break;
    }
  }
}
