# Opti-prod: Solar Production System Optimization
SemesterProject


**Project Overview:**

The Opti-prod project, a fifth-year endeavor, aims to optimize solar production systems through the development of an embedded system. This system is designed to collect weather data, specifically temperature and solar flux (in W/m²), from rooftop installations in photovoltaic solar production sites. Additionally, the project includes the development of an algorithm that correlates real-time weather data with production data from inverters. If a significant and prolonged deviation between expected and actual production is detected, the system triggers an alert (e.g., email, SMS). The system must also be capable of detecting production faults at the inverter level. Both the weather measurement and production calculation/alarm functionalities can be implemented on the same hardware platform. All system data must be accessible via the Modbus TCP protocol through a PC supervisory control system (GTC). The software developed will provide real-time analysis and alerts on the client computer.

**Project Team:**
- Felipe Bartbaste
- Haoyu Wang
- Melvyn Rolland
- Meriam Mhedhbi
- Zhuodong Kang


## Specifications

### General Specifications

The project, a fifth-year initiative, consists of two main parts:

1. **Measurement Module (MM)**: This module is responsible for acquiring physical data such as temperature and solar flux. It comprises two components: the sensor part (MMC) located on the rooftop and the processing part (MMT). The MMC must withstand external environmental factors like rain, wind, and UV radiation. The MMT converts electrical readings into usable temperature and solar flux values and makes them available to the analysis module.

2. **Installation Analysis Module (MAI)**: This module acquires production data from inverters (power, energy, status codes), calculates expected values based on installation and weather data from the MM, analyzes production data, and sends alerts (via email) if a fault or anomaly is detected. The software developed provides real-time analysis and alerts on the client computer.

### Measurement Module Specifications (MM)

- Consists of two parts: MMC (external rooftop sensors) and MMT (processing unit).
- Maximum distance between MMC and MMT: 100 meters with a maximum of 4 wires.
- Low power consumption.
- Capable of calculating daily average temperature and cumulative energy received in kWh/m².
- All data, both instantaneous and calculated, accessible via Modbus TCP protocol.
- Provides a USB serial port for configuration, sensor calibration, data inspection, and real-time communication monitoring.
- Equipped with LEDs for power status, module status, and fault indication.
- Includes a reset/reboot button and software watchdog for module recovery.

### Installation Analysis Module Specifications (MAI)

- Capable of managing up to 10 inverters.
- Acquires data from inverters and weather data (from MM) via Modbus TCP.
- Calculates expected power with high precision.
- Compares expected power to actual power and sends emails to notify stakeholders of prolonged anomalies.
- Maintains a log of operation, including timestamped records of anomalies and faults.
- Web-based user interface for configuration, adjustment of variables/parameters, real-time data inspection, and monitoring of communication with inverters and MM.
- Ability to reset alarm flags.

These specifications outline the minimum hardware and software requirements for the system and its components, ensuring the project's success in optimizing solar production systems and providing real-time analysis and alerts on the client computer.