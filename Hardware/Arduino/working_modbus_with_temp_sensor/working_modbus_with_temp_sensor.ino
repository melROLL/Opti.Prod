#include <SPI.h>
#include <Wire.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(10, 3, 7, 8);


int adc0_result;

Adafruit_BME680 bme;

EthernetServer ethServer(502);
ModbusTCPServer modbusTCPServer;

//const int ledPin = LED_BUILTIN;

void setup() {

  Ethernet.init(10);
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  Serial.println("Ethernet Modbus TCP");
  Ethernet.begin(mac, ip);
  Serial.print("heyy: ");
  Serial.print(Ethernet.localIP());

  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) {
      delay(1);
    }
  }

  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1)
      ;
  }

  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected.");
  }

  ethServer.begin();

  if (!modbusTCPServer.begin()) {
    Serial.println("Failed to start Modbus TCP Server!");
    while (1)
      ;
  }

  modbusTCPServer.configureHoldingRegisters(0x00, 20);  // Configure 1 holding register at address 0x00


  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);
}

void loop() {
  EthernetClient client = ethServer.available();


  if (client) {
    Serial.println("new client");
    modbusTCPServer.accept(client);

    while (client.connected()) {

      if (!bme.performReading()) {
        Serial.println("Failed to perform reading :(");
        return;
      }
      modbusTCPServer.poll();
      delay(5);
      Serial.println("temp1");
      Serial.println(bme.temperature);
      modbusTCPServer.holdingRegisterWrite(0x00, bme.temperature);
     




      // Update the holding register value
      //modbusTCPServer.holdingRegisterWrite(0x00, myData);
    }
    Serial.println("temp1");
    Serial.println(bme.temperature);
    Serial.println("client disconnected");
  }
}
