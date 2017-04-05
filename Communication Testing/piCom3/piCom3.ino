/* Simple Serial ECHO script : Written by ScottC 04/07/2012 */
/* Stage 2 : Delimiters */

/* Use a variable called byteRead to temporarily store
   the data coming from the computer */

void setup() {                
  // Turn the Serial Protocol ON
  Serial.begin(9600);
  //calibrate();
}

void loop() {
  long positions[2]; // Array of desired stepper positions
  String content[2]={"",""};
  byte incomingByte;
  int i = 0;

  while(Serial.available()) {
      incomingByte = Serial.read();
      if(incomingByte == 44){
        i++;
      }
      else{
        content[i].concat((char)incomingByte);
      }
      delay(1);
    }
          
    positions[0] = content[0].toInt();
    positions[1] = content[1].toInt();

  if (content[0] != "" && content[0] !="") {
    //Serial.println(positions[0]);
    //Serial.println(positions[1]);
    Serial.println("Position Recieved");
  }
}

void calibrate(){
  while(!Serial.available()){
    delay(10);
    Serial.println("Connected");
  }
}

