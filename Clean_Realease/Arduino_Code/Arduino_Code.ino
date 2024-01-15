// How to connect the BME on an Arduino Mega:
// - Connect the BME VCC to 5V on the Arduino
// - Connect the BME GND to the Arduino GND
// - Connect the BME SCL to the Arduino 21 pin
// - Connect the BME SDA to the Arduino 20 pin

#include <SPI.h>
#include <Wire.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>   // This is the principal library :)
#include "OneWire.h"            // Include the OneWire library for communication with the sensor
#include "DallasTemperature.h"  // Include the DallasTemperature library for managing the sensor
#include <EMailSender.h>

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define ANCHO_PANTALLA 128  // Width of the OLED screen
#define ALTO_PANTALLA 64    // Height of the OLED screen

#define SEALEVELPRESSURE_HPA (1013.25)

// For the DS18B20 sensor (temperature)
OneWire oneWire(A1);             // Create a OneWire object to communicate with the sensor on pin A1
DallasTemperature ds(&oneWire);  // Create a DallasTemperature object and associate it with the OneWire object

// Define MAC & IP address for the Ethernet shield
// The IP address needs to be on the same network
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(10, 3, 7, 8);

// Initialize the BME sensor
Adafruit_BME680 bme;

Adafruit_SSD1306 display(ANCHO_PANTALLA, ALTO_PANTALLA, &Wire, -1);

// Define the port for Modbus communication (502 by default)
EthernetServer ethServer(502);

// Initialize the Modbus server
ModbusTCPServer modbusTCPServer;
int state = 1;  // Variable to store system state

// Email settings
IPAddress serverIP(66, 228, 43, 14);  // Replace with the actual IP address of mail.smtp2go.com
int serverPort = 2525;                // SMTP server port
EthernetClient emailClient;
const char* senderEmail = "haoyu.wang@epfedu.fr";            // Replace with your sender email address
const char* pwd = "6XCLZWnGzEVDGZDQ";                        // Replace with your sender email address
const char* recipientEmail = "recovery.mary2000@gmail.com";  // Replace with the recipient email address

const int Surface = 2;
const int ProducedEnergyValue = 1;

void setup() {
  Ethernet.init(10);
  Serial.begin(9600);
  while (!Serial) {
    // Wait for the serial connection to be established
  }
  Serial.println("Ethernet Modbus TCP");
  Ethernet.begin(mac, ip);
  // Check the IP address
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

  // Start the Ethernet server
  ethServer.begin();

  if (!modbusTCPServer.begin()) {
    Serial.println("Failed to start Modbus TCP Server!");
    while (1)
      ;
  }
  // Configure the Modbus holding registers
  modbusTCPServer.configureHoldingRegisters(0x00, 20);  // Configure 1 holding register at address 0x00

  // Set up oversampling and filter initialization for BME sensor
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);

  // Initialize DS18B20 sensor
  ds.begin();
}

void loop() {
  // Find the Modbus client
  EthernetClient client = ethServer.available();

  if (client) {
    Serial.println("new client");
    modbusTCPServer.accept(client);

    while (client.connected()) {
      // Read flux sensor value
      int fluxSensorValue = analogRead(A0);
      Serial.print("Flux Value: ");
      Serial.println(fluxSensorValue);

      // Read BME sensor data
      if (!bme.performReading()) {
        Serial.println("Failed to perform reading :(");
        return;
      }

      // Temperature Measurement from DS18B20 sensor
      ds.requestTemperatures();
      float temp = ds.getTempCByIndex(0);

      // Poll Modbus server
      modbusTCPServer.poll();
      delay(5);
      Serial.println("temp");
      Serial.println(bme.temperature);
      Serial.print("Temperature 2: ");
      Serial.print(temp);

      // Swap bytes for Modbus compatibility
      uint16_t swappedPressureData = swapBytes(bme.pressure);
      uint16_t swappedgazResistanceData = swapBytes(bme.gas_resistance);

      // Add sensor values to Modbus holding registers
      modbusTCPServer.holdingRegisterWrite(0x00, bme.temperature);
      modbusTCPServer.holdingRegisterWrite(0x01, bme.pressure);
      modbusTCPServer.holdingRegisterWrite(0x02, bme.gas_resistance);
      modbusTCPServer.holdingRegisterWrite(0x03, bme.humidity);
      modbusTCPServer.holdingRegisterWrite(0x04, fluxSensorValue);
      modbusTCPServer.holdingRegisterWrite(0x05, temp);
      modbusTCPServer.holdingRegisterWrite(0x06, ProducedEnergyValue);
      modbusTCPServer.holdingRegisterWrite(0x07, fluxSensorValue * Surface);
      modbusTCPServer.holdingRegisterWrite(0x08, state);
      modbusTCPServer.holdingRegisterWrite(0x09, Surface);

      // Email condition
      if (fluxSensorValue * Surface > ProducedEnergyValue * 0.2) {
        state = 0;
        modbusTCPServer.holdingRegisterWrite(0x08, state);
        Ethernet.init(10);
        Ethernet.begin(mac);
        checkSMTPServer();
        Ethernet.begin(mac, ip);
      }

      ////////////////////////

      // Initialize the OLED display
      if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        #ifdef __DEBUG__
          Serial.println("Display Not found");  // Display not found
        #endif
        while (true)
          ;
      }

      // Clear display
      display.clearDisplay();

      // Set text size
      display.setTextSize(1);

      // Set text color
      display.setTextColor(SSD1306_WHITE);

      // Set text position
      display.setCursor(3, 8);

      // Display text
      display.println("   MoniMoney ");
      display.println("   ");
      display.print("Temperature: ");
      display.print(bme.temperature);
      display.println("   ");
      display.print("Flux: ");
      display.println(fluxSensorValue);
      display.println("   ");
      display.print("State: ");
      display.println(state);

      // Send to the display
      display.display();
    }

    Serial.println("client disconnected");
  }
}

// Function to swap bytes for Modbus compatibility
uint16_t swapBytes(uint16_t value) {
  return (value >> 8) | (value << 8);
}

// Email functions

void checkSMTPServer() {
  if (emailClient.connect(serverIP, serverPort)) {
    Serial.println("Connected to SMTP server");

    // Read and print the response from the server
    while (emailClient.available()) {
      char c = emailClient.read();
      Serial.print(c);
    }

    // Send EHLO command to the server
    emailClient.println("EHLO example.com");
    delay(500);  // Wait for server response

    // Read and print the response from the server
    while (emailClient.available()) {
      char c = emailClient.read();
      Serial.print(c);
    }

    // Authentication
    Serial.println(F("Sending auth login"));
    emailClient.println("auth login");
    if (!eRcv()) return 0;

    Serial.println(F("Sending User"));
    emailClient.println("aGFveXUud2FuZ0BlcGZlZHUuZnI=");
    if (!eRcv()) return 0;

    Serial.println(F("Sending Password"));
    emailClient.println("NlhDTFpXbkd6RVZER1pEUQ==");
    delay(500);

    // Send MAIL FROM command
    emailClient.println("MAIL FROM:<" + String(senderEmail) + ">");
    delay(500);

    // Read and print the response from the server
    while (emailClient.available()) {
      char c = emailClient.read();
      Serial.print(c);
    }

    // Send RCPT TO command
    emailClient.println("RCPT TO:<" + String(recipientEmail) + ">");
    delay(500);

    // Send DATA command
    emailClient.println("DATA");
    delay(500);
    emailClient.println("Subject: Monitoring Email\r\n");

    emailClient.println("*** WARNING ***This is from The monitoring system, there is an issue with the solar panel!");

    emailClient.println(".");

    Serial.println(F("Sending email"));

    // Read and print the response from the server
    while (emailClient.available()) {
      char c = emailClient.read();
      Serial.print(c);
    }

    delay(500);

    // Read and print the response from the server
    while (emailClient.available()) {
      char c = emailClient.read();
      Serial.print(c);
    }

    delay(1000);

    // Read and print the response from the server
    while (emailClient.available()) {
      char c = emailClient.read();
      Serial.print(c);
    }

    // Send QUIT command
    emailClient.println("QUIT");
    delay(500);

    // Read and print the response from the server
    while (emailClient.available()) {
      char c = emailClient.read();
      Serial.print(c);
    }

    // Close the connection
    emailClient.stop();
  } else {
    Serial.println("Failed to connect to SMTP server");
    Serial.println(emailClient.status());
  }
}

byte eRcv() {
  byte respCode;
  byte thisByte;
  int loopCount = 0;

  while (!emailClient.available()) {
    delay(1);
    loopCount++;

    // If nothing received for 10 seconds, timeout
    if (loopCount > 10000) {
      emailClient.stop();
      Serial.println(F("\r\nTimeout"));
      return 0;
    }
  }

  respCode = emailClient.peek();

  while (emailClient.available()) {
    thisByte = emailClient.read();
    Serial.write(thisByte);
  }

  if (respCode >= '4') {
    efail();
    return 0;
  }

  return 1;
}

void efail() {
  byte thisByte = 0;
  int loopCount = 0;

  emailClient.println(F("QUIT"));

  while (!emailClient.available()) {
    delay(1);
    loopCount++;

    // If nothing received for 10 seconds, timeout
    if (loopCount > 10000) {
      emailClient.stop();
      Serial.println(F("\r\nTimeout"));
      return;
    }
  }

  while (emailClient.available()) {
    thisByte = emailClient.read();
    Serial.write(thisByte);
  }

  emailClient.stop();

  Serial.println(F("disconnected"));
}


