#include <SPI.h>
#include <Ethernet.h>
#include <EMailSender.h>
#include <Base64.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  // Replace with your Ethernet shield MAC address
IPAddress server(66, 228, 43, 14);                    // Replace with the actual IP address of mail.smtp2go.com
int port = 2525;                                      // SMTP server port
EthernetClient client;
//haoyu.wang@epfedu.fr", "6XCLZWnGzEVDGZDQ"
const char* senderEmail = "haoyu.wang@epfedu.fr";            // Replace with your sender email address
const char* pwd = "6XCLZWnGzEVDGZDQ";                        // Replace with your sender email address
const char* recipientEmail = "recovery.mary2000@gmail.com";  // Replace with the recipient email address

void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac);


  Serial.println("******************************************************");
  Serial.println("SMTP Server Check");
  checkSMTPServer();
}

void loop() {
  // Nothing to do in the loop for this example
}

void checkSMTPServer() {
  if (client.connect(server, port)) {
    Serial.println("Connected to SMTP server");

    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }

    // Send EHLO command to the server
    client.println("EHLO example.com");
    delay(500);  // Wait for server response

    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }

    ////
    Serial.println(F("Sending auth login"));
    client.println("auth login");
    if (!eRcv()) return 0;

    Serial.println(F("Sending User"));
    // Change to your base64 encoded user
    //client.println("aGFveXUud2FuZ0BlcGZlZHUuZnI=");
    client.println(encodeBase64(senderEmail));

    if (!eRcv()) return 0;

    Serial.println(F("Sending Password"));
    // change to your base64 encoded password
    //client.println("NlhDTFpXbkd6RVZER1pEUQ==");
    client.println(encodeBase64(pwd));
    delay(500);
    ////

    // Send MAIL FROM command
    client.println("MAIL FROM:<" + String(senderEmail) + ">");
    delay(500);  // Wait for server response

    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }

    // Send RCPT TO command
    client.println("RCPT TO:<" + String(recipientEmail) + ">");
    delay(500);
    // Send DATA command
    client.println("DATA");  // Wait for server response
    delay(500);
    client.println("Subject: Arduino email test\r\n");

    client.println("This is from my Arduino!");

    client.println(".");

    Serial.println(F("Sending email"));


    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }


    delay(500);  // Wait for server response

    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }

    delay(1000);          // Wait for server response

    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }

    // Send QUIT command
    client.println("QUIT");
    delay(500);  // Wait for server response

    // Read and print the response from the server
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }

    // Close the connection
    client.stop();
  } else {
    Serial.println("Failed to connect to SMTP server");
    Serial.println(client.status());
  }
}

byte eRcv() {
  byte respCode;
  byte thisByte;
  int loopCount = 0;

  while (!client.available()) {
    delay(1);
    loopCount++;

    // if nothing received for 10 seconds, timeout
    if (loopCount > 10000) {
      client.stop();
      Serial.println(F("\r\nTimeout"));
      return 0;
    }
  }

  respCode = client.peek();

  while (client.available()) {
    thisByte = client.read();
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

  client.println(F("QUIT"));

  while (!client.available()) {
    delay(1);
    loopCount++;

    // if nothing received for 10 seconds, timeout
    if (loopCount > 10000) {
      client.stop();
      Serial.println(F("\r\nTimeout"));
      return;
    }
  }

  while (client.available()) {
    thisByte = client.read();
    Serial.write(thisByte);
  }

  client.stop();

  Serial.println(F("disconnected"));
}


