/* meArm IK joysticks - York Hackspace May 2014
 * Using inverse kinematics with joysticks
 * Uses two analogue joystcks (two pots each)
 * First stick moves gripper forwards, backwards, left and right
 * Second stick moves gripper up, down, and closes and opens.
 * 
 * I used Sparkfun thumbstick breakout boards, oriented 'upside down'.
 * 
 * Pins:
 * Arduino    Stick1    Stick2    Base   Shoulder  Elbow    Gripper
 *    GND       GND       GND    Brown     Brown   Brown     Brown
 *     5V       VCC       VCC      Red       Red     Red       Red
 *     A0       HOR
 *     A1       VER
 *     A2                 HOR
 *     A3                 VER
 *     11                       Yellow
 *     10                                 Yellow
 *      9                                         Yellow
 *      6                                                   Yellow
 */
#include "meArm.h"
#include <Servo.h>

int basePin = 11;
int shoulderPin = 10;
int elbowPin = 9;
int gripperPin = 6;

int xdirPin = 0;
int ydirPin = 1;
int zdirPin = 3;
int gdirPin = 2;

meArm arm;

// State variables for BCI application
int gripper = -1;
int arm_dir = -1;
int arm_moving = -1;

void setup() {
  Serial.begin(9600);
  arm.begin(basePin, shoulderPin, elbowPin, gripperPin);
}

void loop() {
  // BCI control
  if (Serial.available() > 0) {
    int action = Serial.read();
  
    float theta = arm.getTheta();
    float r = arm.getR();
    float z = arm.getZ();

    switch (action) {
      case 'i':
        1+1;
        break;
      case 'b':
        if (gripper == -1)
          arm.closeGripper();
        else
          arm.openGripper();  
        gripper = -1 * gripper;
        break;    
      case 'l':
        arm.gotoPointCylinder(theta + 0.4, r, z);
        break;    
      case 'r':
        arm.gotoPointCylinder(theta - 0.2, r, z);
        break;    
      case 't':
        arm.gotoPoint(arm.getX(), arm.getY(), z + 5.0 * arm_dir);
        arm_moving = 1;
        break;
      default:
        1+1;
      break;
    }
    
    if (action != 't' && arm_moving == 1) {
      arm_dir = -1 * arm_dir;
      arm_moving = -1; 
    }
  }

  // Joystick control
  float dx = map(analogRead(xdirPin), 0, 1023, -5.0, 5.0);
  float dy = map(analogRead(ydirPin), 0, 1023, 5.0, -5.0);
  float dz = map(analogRead(zdirPin), 0, 1023, 5.0, -5.0);
  float dg = map(analogRead(gdirPin), 0, 1023, 5.0, -5.0);
  if (abs(dx) < 1.5) dx = 0;
  if (abs(dy) < 1.5) dy = 0;
  if (abs(dz) < 1.5) dz = 0;
  
  if (!(dx == 0 && dy == 0 && dz == 0))
    arm.goDirectlyTo(arm.getX() + dx, arm.getY() + dy, arm.getZ() + dz);
  
  if (dg < -3.0)
    arm.closeGripper();
  else if (dg > 3.0)
    arm.openGripper();  

  delay(100);
}
