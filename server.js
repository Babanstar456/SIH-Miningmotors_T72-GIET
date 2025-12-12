const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Store last sensor readings (only stored, no logic)
let sensorData = {
  tds: 0,
  voltage: 0,
  distance_cm: 0,  // ignored for control
  motor_on: false, // follows backend command ONLY
  timestamp: new Date(),
};

// --------------------- OLD TDS ENDPOINT ---------------------
app.post("/api/tds", (req, res) => {
  console.log("Received (TDS legacy):", req.body);

  sensorData.tds = req.body.tds;
  sensorData.voltage = req.body.voltage;
  sensorData.timestamp = new Date();

  res.json({ status: "success" });
});

// --------------------- ESP32 SENSOR ENDPOINT ---------------------
app.post("/api/sensors", (req, res) => {
  console.log("Received ESP32 sensor packet:", req.body);

  // IMPORTANT: motor_on NEVER comes from ESP32 anymore
  sensorData = {
    tds: req.body.tds ?? sensorData.tds,
    voltage: req.body.voltage ?? sensorData.voltage,
    distance_cm: req.body.distance_cm ?? sensorData.distance_cm,
    motor_on: motorCommand,   // always follow backend
    timestamp: new Date(),
  };

  res.json({ status: "ok" });
});

// --------------------- FRONTEND FETCHES SENSOR VALUES ---------------------
app.get("/api/sensors", (req, res) => {
  res.json(sensorData);
});

// --------------------- MOTOR CONTROL ENDPOINTS ---------------------
let motorCommand = true; // OFF by default

app.post("/api/motor/on", (req, res) => {
  motorCommand = true;  // FIXED: TRUE = ON
  console.log("Motor command: ON");
  res.json({ status: "motor_on" });
});

app.post("/api/motor/off", (req, res) => {
  motorCommand = false; // FIXED: FALSE = OFF
  console.log("Motor command: OFF");
  res.json({ status: "motor_off" });
});

// ESP32 polls this
app.get("/api/motor/state", (req, res) => {
  res.json({ motor_on: motorCommand });
});

// --------------------- START SERVER ---------------------
app.listen(3000, () => {
  console.log("API running at http://localhost:3000");
});
