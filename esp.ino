/*
  Unified ESP32 firmware:
  - Reads TDS (analog)
  - Reads SC502 / HC-SR04-style ultrasonic (TRIG/ECHO)
  - Controls 12V relay (active LOW) for motor ON/OFF
  - Polls backend for motor command:
        GET http://10.98.112.93:3000/api/motor/state
  - POST sensor data:
        POST http://10.98.112.93:3000/api/sensors
*/

#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

// ---------- USER CONFIG ----------
const char* WIFI_SSID     = "Galaxy A14 5G AFC6";
const char* WIFI_PASS     = "SwattikA1";

const char* BACKEND_URL   = "http://10.98.112.93:3000/api/sensors";
const char* MOTOR_STATE_URL = "http://10.98.112.93:3000/api/motor/state";

const unsigned long POST_INTERVAL_MS = 1500; 
const unsigned long POLL_INTERVAL_MS = 1200;

// ---------- PIN CONFIG ----------
const int TDS_PIN  = 34;
const int TRIG_PIN = 5;
const int ECHO_PIN = 18;  
const int RELAY_PIN = 26;

// ---------- ADC CONSTANTS ----------
const float ADC_REF = 3.3;
const int ADC_MAX = 4095;
const float TDS_SCALE_K = 500.0;

// ---------- SERVER ----------
WebServer server(80);

// ---------- STATE VARIABLES ----------
volatile bool motorState = false;

unsigned long lastPost = 0;
unsigned long lastPoll = 0;

float lastVoltage = 0.0;
float lastTDSppm = 0.0;
float lastDistanceCM = 0.0;


// ------------------------------------------------------
// SENSOR FUNCTIONS
// ------------------------------------------------------

float readAnalogVoltage(int pin) {
  int raw = analogRead(pin);
  raw = constrain(raw, 0, ADC_MAX);
  return (raw * ADC_REF) / ADC_MAX;
}

float readTDSppm() {
  return readAnalogVoltage(TDS_PIN) * TDS_SCALE_K;
}

float measureDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);
  if (duration == 0) return -1.0;

  return (duration * 0.0343) / 2.0;
}


// ------------------------------------------------------
// RELAY FUNCTIONS
// ------------------------------------------------------
void relayTurnOn() {
  digitalWrite(RELAY_PIN, LOW);
  motorState = true;
  Serial.println("⚡ Relay: MOTOR ON");
}

void relayTurnOff() {
  digitalWrite(RELAY_PIN, HIGH);
  motorState = false;
  Serial.println("⚡ Relay: MOTOR OFF");
}


// ------------------------------------------------------
// POLL BACKEND FOR MOTOR COMMAND
// ------------------------------------------------------
void pollMotorCommand() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(MOTOR_STATE_URL);
  int code = http.GET();

  if (code == 200) {
    String body = http.getString();
    Serial.println("📩 Motor command received: " + body);

    bool backendMotorState = body.indexOf("\"motor_on\":true") > -1;

    if (backendMotorState && !motorState) {
      relayTurnOn();
    }
    else if (!backendMotorState && motorState) {
      relayTurnOff();
    }
  }

  http.end();
}


// ------------------------------------------------------
// POST SENSOR DATA
// ------------------------------------------------------
void postSensorData() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(BACKEND_URL);
  http.addHeader("Content-Type", "application/json");

  String json = "{";
  json += "\"voltage\":" + String(lastVoltage, 3) + ",";
  json += "\"tds\":" + String(lastTDSppm, 2) + ",";
  json += "\"distance_cm\":" + String(lastDistanceCM, 2) + ",";
  json += "\"motor_on\":" + String(motorState ? "true" : "false");
  json += "}";

  int code = http.POST(json);
  Serial.printf("POST %s -> %d\n", BACKEND_URL, code);

  http.end();
}


// ------------------------------------------------------
// HTTP SERVER HANDLERS
// ------------------------------------------------------
void handleRoot() {
  server.send(200, "text/html", "<h2>ESP32 Online</h2>");
}

void handleStatus() {
  String json = "{";
  json += "\"voltage\":" + String(lastVoltage, 3) + ",";
  json += "\"tds\":" + String(lastTDSppm, 2) + ",";
  json += "\"distance_cm\":" + String(lastDistanceCM, 2) + ",";
  json += "\"motor_on\":" + String(motorState ? "true" : "false");
  json += "}";

  server.send(200, "application/json", json);
}


// ------------------------------------------------------
// SETUP
// ------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(TDS_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);

  digitalWrite(RELAY_PIN, HIGH);

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }

  Serial.println("\nWiFi connected!");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/status", handleStatus);
  server.begin();
}


// ------------------------------------------------------
// LOOP
// ------------------------------------------------------
void loop() {
  server.handleClient();

  unsigned long now = millis();

  // -------- Poll motor command every 1.2 seconds ----------
  if (now - lastPoll >= POLL_INTERVAL_MS) {
    lastPoll = now;
    pollMotorCommand();
  }

  // -------- Read sensors + POST every 1.5 seconds ----------
  if (now - lastPost >= POST_INTERVAL_MS) {
    lastPost = now;

    lastVoltage = readAnalogVoltage(TDS_PIN);
    lastTDSppm = readTDSppm();
    lastDistanceCM = measureDistanceCM();

    Serial.printf("V: %.3f  TDS: %.2f  Dist: %.2f  Motor: %s\n",
                  lastVoltage, lastTDSppm, lastDistanceCM,
                  motorState ? "ON" : "OFF");

    postSensorData();
  }

  delay(5);
}
