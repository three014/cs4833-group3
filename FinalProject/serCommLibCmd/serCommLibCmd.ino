/*

 http://www.arduino.cc/en/Tutorial/SerialEvent
 
 */
 
#include <Wire.h>                // include the PRIZM library in the sketch
#include <PRIZM.h>               // include the PRIZM library in the sketch
PRIZM prizm;                     // instantiate a PRIZM object “prizm” so we can use its functions

int stringCounter = 0;
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String outputString = "";        // a string to hold outgoing data

int cmd = 0;                     // an integer to store the cmd
int param = 0;
String cmdStr = "";              // a string to store the cmd
String paramStr = "";

void setup() {
  prizm.PrizmBegin();            // start prizm
  prizm.setMotorInvert(1,1);     // invert the direction of DC Motor 1 to harmonize the direction of opposite facing drive motors
                                 
  Serial.begin(9600);            // initialize serial:
  
  // reserve 20/10 bytes for the string:
  inputString.reserve(20);
  outputString.reserve(20);
  cmdStr.reserve(10);
}

void loop() {
  // when stringComplete is true, we take actions, otherwise we skip
  if (stringComplete) {
    cmdStr = inputString.substring(0,1);  // here we only read the first char, and ignore the remainings.
    paramStr = inputString.substring(1, stringCounter-1);
    cmd = cmdStr.toInt();                  // convert string cmd to integer cmd
    param = paramStr.toInt();

    switch (cmd) {
      // Simple Echo
      case 1:{
        outputString += "1";               
        break;
      }

      // Move Forward
      case 2:{
        outputString += "2";
        prizm.setMotorPowers(param, param);
        break;
      }

      // Move Backward
      case 3:{
        outputString += "3";
        prizm.setMotorPowers(-param, -param);
        break;
      }

      // Turn Left
      case 4:{
        outputString += "4";               
        prizm.setMotorPowers(125,param);      
        break;
      }

      // Turn Right
      case 5:{
        outputString += "5";               
        prizm.setMotorPowers(param,125);      
        break;
      }

      // read sonic sensor connected to D3 on the controller
      case 6:{
        outputString += "6";               
        outputString += prizm.readSonicSensorCM(param); 
        break;
      }

      case 7:{
        outputString += "7";               
        outputString += prizm.readSonicSensorIN(param); 
        break;
      }
      
      case 8:{
        outputString += "8";               
        prizm.setMotorPowers(125,125);
        break;
      }

      case 9:{
        outputString += "9";
        prizm.PrismEnd();
        break
      }
    }
    
    Serial.println(outputString);          // println helps us to send back msg with a '\n' at the end
    
    // clear the variables to wait for another cmd sending
    inputString = "";
    outputString = "";
    cmdStr = "";
    cmd = 0;
    stringComplete = false;                 // reset the flag to make sure we only enter this if condition when the next line of data is received
  }
}


// ************* You do not need to modify the following ***************
// ************* Read the following code will help you understand how it deal with incoming data from serial port **************
/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString
    inputString += inChar;
    stringCounter++;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}


