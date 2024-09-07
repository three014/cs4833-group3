#include <Wire.h>

/*  PRIZM Controller example program
 *  This program will move the TaskBot in a square driving pattern.
 *  author PWU 08/05/2016  
*/
  #include <PRIZM.h>    // include PRIZM library
  PRIZM prizm;          // instantiate a PRIZM object “prizm” so we can use its functions

void setup() {
  prizm.PrizmBegin();         // initialize PRIZM
  prizm.setMotorInvert(1,1);  // invert the direction of DC Motor 1 to harmonize the direction
}
void loop() {
  prizm.setMotorPowers(-60,50);      // go forward at 50% power
  delay(1000);                      // wait here for 2 seconds while motors spin
  prizm.setMotorPowers(125,125);    // stop both motors with in brake mode
  delay(1000);                      // wait here for 1 second
  prizm.setMotorPowers(50,-60);     // make a right turn
  delay(1000);                       // wait here for .75 seconds while motors spin                // wait here for 1 second
  prizm.PrizmEnd();                 // end program and reset PRIZM
}






