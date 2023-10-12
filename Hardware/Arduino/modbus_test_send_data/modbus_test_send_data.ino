#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(10, 3, 7, 8);

int myData = 20;  // Your data, change as needed
int adc0_result;


EthernetServer ethServer(502);
ModbusTCPServer modbusTCPServer;

//const int ledPin = LED_BUILTIN;

void setup() {

  Ethernet.init(10);
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  Serial.println("Ethernet Modbus TCP Example");
  Ethernet.begin(mac, ip);
  Serial.print("heyy: ");
  Serial.print(Ethernet.localIP());

  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
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

  modbusTCPServer.configureHoldingRegisters(0x00, 20);  // Configure 1 holding register at address 0x00

}

void loop() {
  EthernetClient client = ethServer.available();

  if (client) {
    Serial.println("new client");
    modbusTCPServer.accept(client);

    while (client.connected()) {
      modbusTCPServer.poll();
      delay(5);
      updateREG();
       // Update the holding register value
      //modbusTCPServer.holdingRegisterWrite(0x00, myData);
    }

    Serial.println("client disconnected");
  }
}

void updateREG() {
//adc0 = ads.readADC_SingleEnded(1);
modbusTCPServer.holdingRegisterWrite(0x00, myData);
//adc0_result = modbusTCPServer.holdingRegisterRead(0x00);
// Serial.print("AIN0: "); Serial.println(adc0_result);
// Serial.println("i am here ");
}



