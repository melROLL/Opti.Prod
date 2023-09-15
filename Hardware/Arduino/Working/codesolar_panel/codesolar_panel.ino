#define VOLT A1

float volt, volts;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  /*---------Voltage----------*/
  int temp1 = analogRead(VOLT);
  volts = (temp1 / 511.5)*2.5 ;
  delay(10);
  
  /*------Send to Serial------*/
  Serial.print("Voltage: ");
  Serial.print(volts);
  Serial.print("V\t");
  
  Serial.println("Solar Flux: ");

  
  delay(500);
}
