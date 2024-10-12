/*
  Serial Event example
 
 When new serial data arrives, this sketch adds it to a String.
 When a newline is received, the loop prints the string and 
 clears it.
 
 A good test for this is to try it with a GPS receiver 
 that sends out NMEA 0183 sentences. 
 
 Created 9 May 2011
 by Tom Igoe
 
 This example code is in the public domain.
 
 http://www.arduino.cc/en/Tutorial/SerialEvent
 
 */
 
#include <Wire.h>                // include the PRIZM library in the sketch
#include <PRIZM.h>               // include the PRIZM library in the sketch
PRIZM prizm;                     // instantiate a PRIZM object “prizm” so we can use its functions

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String outputString = "";        // a string to hold outgoing data

int cmd = 0;                     // an integer to store the cmd
String cmdStr = "";              // a string to store the cmd

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
    cmdStr = inputString.substring(0,1);   // here we only read the first char, and ignore the remainings. In the future, you can design your own msg format to transfer more information
    cmd = cmdStr.toInt();                  // convert string cmd to integer cmd
    
    switch (cmd) {
      // echo
      case 1:{
        outputString += "1";               
        break;
      }
      // turn left
      case 2:{
        outputString += "2";               
        prizm.setMotorPowers(50,125);      
        break;
      }
      // turn right
      case 3:{
        outputString += "3";               
        prizm.setMotorPowers(125,50);      
        break;
      }
      // read sonic sensor connected to D3 on the controller
      case 4:{
        outputString += "4";               
        outputString += prizm.readSonicSensorCM(3); 
        break;
      }
      // break the motor
      case 5:{
        outputString += "5";               
        prizm.setMotorPowers(125,125);
        break;
      }

      // turn around
      case 6:{
        outputString += "6";
        prizm.setMotorPowers(-20, 20);
        break;
      }

      go straight
      case 7:{
        outputString += "7";
        prizm.setMotorPowers(10, 10);
        break;
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
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}


