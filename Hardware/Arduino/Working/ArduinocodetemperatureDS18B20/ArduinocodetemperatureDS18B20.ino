/*
________          __  .__    __________                   .___
\_____  \ _______/  |_|__|   \______   \_______  ____   __| _/
 /   |   \\____ \   __\  |    |     ___/\_  __ \/  _ \ / __ | 
/    |    \  |_> >  | |  |    |    |     |  | \(  <_> ) /_/ | 
\_______  /   __/|__| |__| /\ |____|     |__|   \____/\____ | 
        \/|__|             \/                              \/
        */
        
#include "OneWire.h"           // Include the OneWire library for communication with the sensor
#include "DallasTemperature.h"  // Include the DallasTemperature library for managing the sensor

OneWire oneWire(A1);            // Create a OneWire object to communicate with the sensor on pin A1
DallasTemperature ds(&oneWire); // Create a DallasTemperature object and associate it with the OneWire object

void setup() {
  Serial.begin(9600);  // Initialize serial communication at a baud rate of 9600 (bits per second)
  ds.begin();          // Initialize the DallasTemperature sensor
}

void loop() {
  ds.requestTemperatures();   // Send a temperature measurement request to the sensor
  int t = ds.getTempCByIndex(0); // Read the temperature in degrees Celsius from the sensor and store it in the 't' variable
 
  Serial.print(t);            // Print the temperature in degrees Celsius
  Serial.println("C");       // Print "C" to indicate the unit of measurement (degrees Celsius)
 
  delay(1000);                // Wait for 1 second before reading the temperature again
}

// Connection:
// A1: Data pin for the DS18B20 sensor (yellow wire)
// 4.7K resistor between VDD and data pin
