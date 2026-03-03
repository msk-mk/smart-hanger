//const int PULSE_PIN = 2;
//const int DIGITAL_READ_PIN = 3;
//const int ANALOG_READ_PIN = 5;

const int PULSE_PIN = 5;
const int DIGITAL_READ_PIN = 6;
const int ANALOG_READ_PIN = 0;

const double E = 5.06; // GPIO電圧実測値
const double R = 2000000; // 2MΩ
const double V = E * 0.632;

void setup()
{
  Serial.begin(9600);
  Serial.print("Connecting...");
  Serial.println();
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

  Serial.print(T);

  Serial.println();
  digitalWrite(PULSE_PIN, LOW);
  delay(2000);
}
