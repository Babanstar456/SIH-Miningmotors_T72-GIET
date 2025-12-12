# 🌞 SURYADUT – Solar-Powered Smart Dewatering System

A complete diesel-free, energy-efficient dewatering solution for mining operations in India.  
SURYADUT integrates **Solar PV**, **Pump-as-Turbine (PaT) energy recovery**, **multi-gear torque optimization**, **magnetic piston assist**, **IoT monitoring**, and **ML-based predictive maintenance** into one intelligent system.

---

## 📌 Project Overview

SURYADUT replaces traditional diesel pumps with a high-efficiency, renewable-powered dewatering system designed for harsh mining conditions.  
The system intelligently manages energy, predicts failures, and maximizes efficiency using:

- 14–16 kWp Solar PV system  
- 25 HP, 120 m head dewatering pump  
- PaT turbine for 1.5–3.5 kW energy recovery  
- Multi-stage gearbox + magnetic/spring pistons  
- IoT telemetry using ESP32  
- Machine learning predictive maintenance  

---

## 🚀 Key Features

### 🔋 Solar Dewatering
- 56–72 kWh/day solar energy
- Runs pump + charges battery with surplus

### ⚙ Pump Operation (25 HP)
- 18.6 kW, 120 m head
- VFD-controlled for high efficiency  
- Smart RPM scaling based on water levels and load

### 🔄 PaT Energy Recovery
- Generates 10–12 kWh/day
- Improves system efficiency by ~20%
- Stabilized via multi-stage gearbox

### 🧲 Magnetic + Spring Pistons
- Positioned at **45° offset**
- Provide low-flow torque boost
- Increase alternator RPM stability

### 📡 IoT Monitoring
Real-time dashboard tracking:

- Solar generation  
- Water pumped  
- Pump energy use  
- Water level  
- TDS  
- Flow & pressure  
- Turbine RPM  
- Gear vibration & temperature  

### 🤖 ML Predictive Maintenance
Detects:

- Bearing wear  
- Cavitation  
- Gearbox faults  
- Torque fluctuations  
- Pump efficiency drop  
- Temperature anomalies  

Outputs:

- Failure predictions (RUL)  
- Maintenance scheduling  
- Auto-load adjustments  

---

## 🏗 System Architecture


---

## 🧩 Hardware Components

### Mechanical
- 25 HP vertical dewatering pump  
- PaT turbine (reverse centrifugal)
- Multi-stage gearbox  
- Dual magnetic piston torque assist  
- Alternator (1500 RPM)

### Sensors
- Ultrasonic water level  
- TDS probe  
- Flow meter  
- Pressure transducers  
- Current sensors (INA219)  
- Temperature sensors  
- MPU6050 vibration  
- Hall RPM sensors

### Electronics
- ESP32 Controller  
- LAN Communication  
- VFD  
- Solar inverter  
- BESS battery  
- Protection: MCCB, SPD, RCD, earthing  

---

## 🧪 Software Stack

### Firmware (ESP32)
- C++ (Arduino)  
- Sensor drivers  
- Motor control (Modbus, PWM)  
- Safety automation  
- WebSocket/HTTP communication  

### Backend
- Node.js  
- REST + WebSocket API  
- Telemetry handler  
- Energy calculations  
- ML model inference  

### Dashboard
- HTML, CSS, JavaScript  
- Live telemetry  
- Pump control  
- Cycle history  
- System analytics  

### ML Models
- Anomaly detection  
- LSTM/GRU RUL prediction  
- Torque prediction models  

---

## 📊 Energy Performance

| Parameter | Value |
|-----------|--------|
| Solar generation | 56–72 kWh/day |
| Pump power (optimized) | 48–54 kWh/day |
| PaT energy recovery | 10–12 kWh/day |
| Net surplus | 8–12 kWh/day |
| Diesel replaced | 16 L/day |
| Annual savings | ₹5.31 lakh per pump |

---

## 🛡 Safety & Protection

- Dry-run detection  
- Overcurrent shutoff  
- High-temperature trip  
- Gearbox overheat throttle  
- Overflow prevention  
- Manual override  

---

## 📁 Suggested Repository Structure

