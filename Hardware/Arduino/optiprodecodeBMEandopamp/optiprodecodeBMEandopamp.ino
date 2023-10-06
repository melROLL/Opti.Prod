/*!
BME680 to Arduino VCC and GND:

Connect the VCC (Voltage) pin of the BME680 to the 3.3V output on the Arduino.
Connect the GND (Ground) pin of the BME680 to one of the GND pins on the Arduino.
BME680 to Arduino SDA and SCL (I2C):

Connect the SDA (Serial Data) pin of the BME680 to the SDA (A4) pin on the Arduino.
Connect the SCL (Serial Clock) pin of the BME680 to the SCL (A5) pin on the Arduino.
BME680 to Arduino VIN (Optional):

If your BME680 operates at 5V, you should connect it to the 5V output on the Arduino. However, many BME680 sensors operate at 3.3V, so connecting it to the 3.3V output is usually sufficient.

We also need the connect the PV sensor in the pin A0 of tha arduino 
 */


#include <Wire.h>

#define BME680_I2C_ADDR 0x76

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Wire.begin();

  // Initialize the BME680 sensor
  if (!initBME680()) {
    Serial.println("Unable to find a valid BME680 sensor, check the wiring!");
    while (1);
  }

  // Set oversampling and filter initialization
  setBME680Oversampling();

  // Print sensor details
  Serial.println("BME680 Sensor found!");
}

void loop() {
  // Read analog value from pin A0
  int sensorValue = analogRead(A0);

  // Print the value on the Serial Monitor
  Serial.print("Analog Value: ");
  Serial.println(sensorValue);

  float temperature, humidity, pressure, gas_resistance;
  if (readBME680Data(temperature, humidity, pressure, gas_resistance)) {
    Serial.print("Temperature = ");
    Serial.print(temperature);
    Serial.println(" *C");

    Serial.print("Humidity    = ");
    Serial.print(humidity);
    Serial.println(" %");

    Serial.print("Pressure    = ");
    Serial.print(pressure / 100.0); // Convert pressure to hPa
    Serial.println(" hPa");

    Serial.print("Gas         = ");
    Serial.print(gas_resistance / 1000.0); // Convert gas resistance to KOhm
    Serial.println(" KOhm");
  } else {
    Serial.println("Reading failed :(");
  }

  Serial.println();

  delay(1000); // Wait for 1 second before the next reading
}

bool initBME680() {
  Wire.beginTransmission(BME680_I2C_ADDR);
  Wire.write(0x73); // Soft reset command
  Wire.endTransmission();
  delay(10);

  // Check if the chip ID matches that of BME680 (0x61)
  Wire.beginTransmission(BME680_I2C_ADDR);
  Wire.write(0xD0);
  Wire.endTransmission();
  Wire.requestFrom(BME680_I2C_ADDR, 1);
  if (Wire.available() && Wire.read() == 0x61) {
    return true;
  }
  return false;
}

void setBME680Oversampling() {
  // Set oversampling and filter settings
  Wire.beginTransmission(BME680_I2C_ADDR);
  Wire.write(0x74); // Humidity oversampling
  Wire.write(0x02); // 2x oversampling
  Wire.endTransmission();

  Wire.beginTransmission(BME680_I2C_ADDR);
  Wire.write(0x72); // Temperature oversampling
  Wire.write(0x08); // 8x oversampling
  Wire.endTransmission();

  Wire.beginTransmission(BME680_I2C_ADDR);
  Wire.write(0x75); // Pressure oversampling
  Wire.write(0x04); // 4x oversampling
  Wire.endTransmission();

  Wire.beginTransmission(BME680_I2C_ADDR);
  Wire.write(0x64); // Heater control
  Wire.write(0x32); // 320°C, 150ms
  Wire.endTransmission();
}

bool readBME680Data(float &temperature, float &humidity, float &pressure, float &gas_resistance) {
  Wire.beginTransmission(BME680_I2C_ADDR);
  Wire.write(0x73); // Gas measurement
  Wire.endTransmission();
  Wire.requestFrom(BME680_I2C_ADDR, 6);

  if (Wire.available() >= 6) {
    uint32_t raw_data = 0;
    for (int i = 0; i < 3; i++) {
      raw_data |= (uint32_t)Wire.read() << (i * 8);
    }
    gas_resistance = (float)raw_data;

    for (int i = 0; i < 3; i++) {
      raw_data |= (uint32_t)Wire.read() << (i * 8);
    }
    temperature = (float)(raw_data - 256000) / 100.0;

    for (int i = 0; i < 3; i++) {
      raw_data |= (uint32_t)Wire.read() << (i * 8);
    }
    humidity = (float)raw_data / 1000.0;

    Wire.beginTransmission(BME680_I2C_ADDR);
    Wire.write(0x74); // Pressure measurement
    Wire.endTransmission();
    Wire.requestFrom(BME680_I2C_ADDR, 3);

    if (Wire.available() >= 3) {
      raw_data = 0;
      for (int i = 0; i < 3; i++) {
        raw_data |= (uint32_t)Wire.read() << (i * 8);
      }
      pressure = (float)raw_data;
      return true;
    }
  }

  return false;
}
