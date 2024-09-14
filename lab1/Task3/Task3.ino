#include <PRIZM.h>

#include <Wire.h>

PRIZM prizm;

int halfCombinedVert, combinedVert, vert1, vert2;
int halfCombinedHorz, combinedHorz, horz1, horz2;

int isCentered = 0;
int isCenteredVert = 0;
int isCenteredHorz = 0;


void setup() {
  // put your setup code here, to run once:
  prizm.PrizmBegin();

  Serial.begin(9600);
  
  prizm.setMotorInvert(1,1);
  
  vert1 = prizm.readSonicSensorCM(3);
  prizm.setMotorPowers(-15, 15);
  delay(1600);
  prizm.setMotorPowers(125, 125);
  delay(1000);
  Serial.println(vert1);

  horz1 = prizm.readSonicSensorCM(3);
  prizm.setMotorPowers(-15, 15);
  delay(1600);
  prizm.setMotorPowers(125, 125);
  delay(1000);
  Serial.println(horz1);

  vert2 = prizm.readSonicSensorCM(3);
  prizm.setMotorPowers(-15, 15);
  delay(1625);
  prizm.setMotorPowers(125, 125);
  delay(1000);
  Serial.println(vert2);

  horz2 = prizm.readSonicSensorCM(3);
  prizm.setMotorPowers(-15, 15);
  delay(1625);
  prizm.setMotorPowers(125, 125);
  delay(1000);
  Serial.println(horz2);

  combinedVert = vert1 + vert2;
  combinedHorz = horz1 + horz2;
  
  halfCombinedVert = combinedVert / 2;
  halfCombinedHorz = combinedHorz / 2;
 
  Serial.println(combinedVert);
  Serial.println(combinedHorz);

}

void loop() {
  // put your main code here, to run repeatedly:
        //prizm.PrizmEnd();
    while (!isCenteredVert) {
      if (prizm.readSonicSensorCM(3) > halfCombinedVert + 5) {
        prizm.setMotorPowers(15, 15);
      } else if (prizm.readSonicSensorCM(3) < halfCombinedVert - 5) {
          prizm.setMotorPowers(-15, -15);
      } else {
        prizm.setMotorPowers(125, 125);
        isCenteredVert = 1;
      }
    }
    
    Serial.println();
    Serial.println(prizm.readSonicSensorCM(3));  
    prizm.setMotorPowers(-15, 15);
    delay(1600); 
    
    while (!isCenteredHorz) {
      if (prizm.readSonicSensorCM(3) > halfCombinedHorz + 5) {
        prizm.setMotorPowers(15, 15);
      } else if (prizm.readSonicSensorCM(3) < halfCombinedHorz - 5){
        prizm.setMotorPowers(-15, -15);
      } else {
        prizm.setMotorPowers(125, 125);
        isCenteredHorz = 1;
      }
    }      
    
    prizm.setMotorPowers(125, 125);   
    Serial.println(prizm.readSonicSensorCM(3));
    prizm.PrizmEnd();
}

