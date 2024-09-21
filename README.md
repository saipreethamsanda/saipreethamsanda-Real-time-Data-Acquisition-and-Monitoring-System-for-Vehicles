
# Real-Time Data Acquisition and Monitoring System for Automobiles

## Project Overview
This project aims to design and develop a system that collects real-time data from various sensors in automobiles, such as vehicle speed, engine temperature, fuel level, and tire pressure. The system continuously monitors these parameters and alerts drivers or service centers about anomalies or critical conditions, improving vehicle safety and performance optimization.

## Features
- **Real-time Monitoring:** Displays vehicle data such as speed, temperature, and fuel level on a dashboard.
- **Alert System:** Sends notifications and alerts when critical thresholds are breached (e.g., high temperature).
- **Data Collection:** Gathers sensor data using microcontrollers and transmits it to a user-friendly dashboard for visualization.
- **Predictive Maintenance:** Provides insights into vehicle health, enabling predictive maintenance to improve longevity and performance.

## System Components
- **Microcontroller:** STM32 NUCLEO
- **Sensors:**
  - Temperature Sensor (DHT11)
  - Fuel Level Sensor
  - Hall Effect Sensor (LM393)
  - Brake System (Tactile Push Button Switch)
- **Communication Protocol:** Data is transmitted using USB serial communication and processed with Python.

## Software Design
The software includes a Python-based GUI for real-time data visualization and alert management. The GUI is built using the Tkinter library, and serial communication with the STM32 microcontroller is established using PySerial.

- **Main Functions:**
  - Dashboard with real-time vehicle data (speed, RPM, temperature, fuel level).
  - Alerts and warnings based on critical thresholds (e.g., high engine temperature).
  - Data processing and visualization.
  
## Hardware Design
The hardware setup includes:
- STM32 Nucleo microcontroller.
- DHT11 for temperature measurement.
- A hall-effect sensor for speed/RPM measurement.
- Fuel level sensor.
- Tactile push button switch for brake status detection.


4. **Connect the Hardware:**
   Ensure all sensors are connected to the microcontroller as per the hardware design SCHEMATIC.png.
   


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
-Here is the updated acknowledgments section:

---

## Acknowledgements
This project was developed by:
- **Sai Preetham Sanda**
- **Boya Dileep**
- **Kishore Kumar**
- **Dasari Charan**

- Special thanks to KPIT for providing the platform and resources for this project.

---
