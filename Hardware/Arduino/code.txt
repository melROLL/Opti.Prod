
#include "OneWire.h"           // Inclure la bibliothèque OneWire pour la communication avec la sonde
#include "DallasTemperature.h"  // Inclure la bibliothèque DallasTemperature pour la gestion de la sonde

OneWire oneWire(A1);            // Créer un objet OneWire pour communiquer avec la sonde sur la broche A1
DallasTemperature ds(&oneWire); // Créer un objet DallasTemperature et le lier à l'objet OneWire

void setup() {
  Serial.begin(9600);  // Initialiser la communication série à une vitesse de 9600 bauds (bits par seconde)
  ds.begin();          // Initialiser la sonde DallasTemperature
}

void loop() {
  ds.requestTemperatures();   // Envoyer une demande de mesure de température à la sonde
  int t = ds.getTempCByIndex(0); // Lire la température en degrés Celsius depuis la sonde et la stocker dans la variable 't'
 
  Serial.print(t);            // Afficher la température en degrés Celsius
  Serial.println( "C");       // Afficher "C" pour indiquer l'unité de mesure (degrés Celsius)
 
  delay(1000);                // Attendre 1 seconde avant de lire à nouveau la température
}


// branchement

//A1 le data du ds18B20 (jaune)
// resistor de 4.7K entre VDD et data
