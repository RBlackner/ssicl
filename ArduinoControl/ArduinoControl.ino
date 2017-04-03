//-----------------------------------------------------------------
//library setup
//-----------------------------------------------------------------

//-----------------------------------------------------------------
//io pin setup
//-----------------------------------------------------------------
const int lightSwitch = 13;
//-----------------------------------------------------------------
//constant varibles
//-----------------------------------------------------------------

//-----------------------------------------------------------------
//global varibles
//-----------------------------------------------------------------
bool light_on = false;
void setup()
{     
    Serial.begin(9600);
    //communication intialization between RPI and Arduino
    intialization();
    // initialize I/O
    pinMode(lightSwitch, OUTPUT);
}

void loop(){
  long positions[2]; // Array of desired stepper positions
  String function;
  String content[3]={"","",""};
  String messageToPi = "";
  byte incomingByte;
  int i = 0;

  if(Serial.available()){
    while(Serial.available()) {
        incomingByte = Serial.read();
        if(incomingByte == 44 || incomingByte == 58){
          i++;
        }
        else{
          content[i].concat((char)incomingByte);
        }
        delay(10);
    }
    function = content[0];
    if(function == "Light On"){
      if(light_on){
        digitalWrite(lightSwitch,LOW);
        light_on = false;
        messageToPi = function+':'+"False";
        }
      else{
        digitalWrite(lightSwitch,HIGH);
        light_on = true;
        messageToPi = function+':'+"True";
        }
        Serial.println(messageToPi);
    }
    else if(function == "Ping"){
      messageToPi = ','+',';
      Serial.println(messageToPi);
    }
  }
}

void intialization(){
  String content="";
  byte incomingByte;
  int i = 0;
  while(!Serial.available());
  while(Serial.available()) {
      incomingByte = Serial.read();
      content.concat((char)incomingByte);
      delay(10);
    }
  if(content!= "") {
    Serial.println("Initialized:True");
  }
  else{
    Serial.println("Initialized:False");
  }
}

//-----------------------------------------------------------------
//Untested method
//-----------------------------------------------------------------
