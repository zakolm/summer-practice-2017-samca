String in_data;

void setup() 
{
  Serial.begin(9600);
  Serial.println("Connect");
  pinMode (9, OUTPUT);
  in_data="";
}
void transmit()
{
  for (int i=0; i<in_data.length(); i++)
      {
        if (in_data[i]=='1')
            digitalWrite(9,HIGH);
        if (in_data[i]=='2')
            digitalWrite(10,HIGH);
        if (in_data[i]=='3')
          {
            digitalWrite(9,LOW);
            digitalWrite(10,LOW);
          }
        delay(1000);
      }
}
void loop() 
{
  if (Serial.available()>0)
  {
    char chr=Serial.read();
    if (chr!='0')
    {
      if(chr=='t')
        Serial.println("t");
      else
        in_data+=chr;
    }
    else
    {
      transmit();
      in_data="";
    }
  }
 
}
