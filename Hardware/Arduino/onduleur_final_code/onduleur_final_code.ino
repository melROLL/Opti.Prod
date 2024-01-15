#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(10, 3, 7, 8);

EthernetServer ethServer(502);
ModbusTCPServer modbusTCPServer;

const int ledPin = 13;  // Assuming you have an LED connected to pin 13
int registerValue = 0;

void setup() {
  Ethernet.init(10);
  Serial.begin(9600);
  while (!Serial) {
    ; 
  }
  Serial.println("Ethernet Modbus TCP Example");
  Ethernet.begin(mac, ip);
  Serial.print("IP Address: ");
  Serial.println(Ethernet.localIP());

  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found. Sorry, can't run without hardware. :(");
    while (true) {
      delay(1);
    }
  }
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected.");
  }

  ethServer.begin();

  if (!modbusTCPServer.begin()) {
    Serial.println("Failed to start Modbus TCP Server!");
    while (1);
  }

  modbusTCPServer.configureHoldingRegisters(0x00, 1);
}

void loop() {
  EthernetClient client = ethServer.available();

  if (client) {
    Serial.println("new client");
    modbusTCPServer.accept(client);

    while (client.connected()) {
      modbusTCPServer.poll();
      delay(1000);

      // Read holding register value
      int data = modbusTCPServer.holdingRegisterRead(0x00);
      Serial.print("Read data: ");
      Serial.println(data);
       
      
    }

    Serial.println("client disconnected");
  }
}
