//how to connect the bme on an arduino mega
//first the bme vcc to 5v on the arduino
//the bme GND to the arduino GND
//the bme SCL to the arduino 21 pin
//the bme SDA to the arduino 20 pin

#include <SPI.h>
#include <Wire.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h> //this is the principal library :)
#include "OneWire.h"           // Include the OneWire library for communication with the sensor
#include "DallasTemperature.h"  // Include the DallasTemperature library for managing the sensor

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define ANCHO_PANTALLA 128 // ancho pantalla OLED
#define ALTO_PANTALLA 64 // alto pantalla OLED

#define SEALEVELPRESSURE_HPA (1013.25)

//for the DS18B20 sensor(temperture)
OneWire oneWire(A1);            // Create a OneWire object to communicate with the sensor on pin A1
DallasTemperature ds(&oneWire); // Create a DallasTemperature object and associate it with the OneWire object

//define mac & ip address for the ethernet shield
//the ip address needs to be on the same network
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(10, 3, 7, 8);

//initialize the sensor
Adafruit_BME680 bme;

Adafruit_SSD1306 display(ANCHO_PANTALLA, ALTO_PANTALLA, &Wire, -1);

//define the port of modbus communication 502 by defualt
EthernetServer ethServer(502);

//initialize the server
ModbusTCPServer modbusTCPServer;


void setup() {

  Ethernet.init(10);
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  Serial.println("Ethernet Modbus TCP");
  Ethernet.begin(mac, ip);
  //check the ip address
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

 

//start the ethernet serveer
  ethServer.begin();

  if (!modbusTCPServer.begin()) {
    Serial.println("Failed to start Modbus TCP Server!");
    while (1)
      ;
  }
//configure the modbus holding registers
  modbusTCPServer.configureHoldingRegisters(0x00, 20);  // Configure 1 holding register at address 0x00


  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);

  //DS18B20 sensor
  ds.begin();  



}


void loop() {
  //find the modbus client
  EthernetClient client = ethServer.available();


  if (client) {
    Serial.println("new client");
    modbusTCPServer.accept(client);

    while (client.connected()) {
      int fluxSensorValue = analogRead(A0);
      Serial.print("Flux Value: ");
      Serial.println(fluxSensorValue);

      if (!bme.performReading()) {
        Serial.println("Failed to perform reading :(");
        return;
      }

      // Temperature Measurement
      ds.requestTemperatures();   // Send a temperature measurement request to the sensor
      float temp = ds.getTempCByIndex(0); // Read the temperature in degrees Celsius from the sensor and store it in the 't' variable

      modbusTCPServer.poll();
      delay(5);
      Serial.println("temp");
      Serial.println(bme.temperature);
      Serial.print("Temperature 2: ");
      Serial.print(temp);   

      uint16_t swappedPressureData = swapBytes(bme.pressure);
      uint16_t swappedgazResistanceData = swapBytes(bme.gas_resistance);

      //add the sensor values to the modbus holding registers and read them on the modbusPoll software
      modbusTCPServer.holdingRegisterWrite(0x00, bme.temperature);
      modbusTCPServer.holdingRegisterWrite(0x01, bme.pressure);  
      modbusTCPServer.holdingRegisterWrite(0x02, bme.gas_resistance);  
      modbusTCPServer.holdingRegisterWrite(0x03, bme.humidity);
      modbusTCPServer.holdingRegisterWrite(0x04, fluxSensorValue);
      modbusTCPServer.holdingRegisterWrite(0x05, temp);



  ////////////////////////

   if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
#ifdef __DEBUG__
    Serial.println("No se encuentra la pantalla OLED");
#endif
    while (true);
  }
  // Tamaño del texto
  display.clearDisplay();
    // Tamaño del texto
  display.setTextSize(1);
  // Color del texto
  display.setTextColor(SSD1306_WHITE);
  // Posición del texto
  display.setCursor(3, 8);
  // Escribir texto
  display.println("   MoniMoney ");
  display.println("   ");
  display.print("Temperature: ");
  display.print(bme.temperature);
  display.println("   ");
  display.print("Flux: ");
  display.println(fluxSensorValue);
  display.println("   ");
  display.print("State: ");
  display.println(0);

  // Enviar a pantalla
  display.display();


    }
    Serial.println("client disconnected");
  }
}

//to make it compatible with modbus registers
uint16_t swapBytes(uint16_t value) {
    return (value >> 8) | (value << 8);
}