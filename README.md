# RpiAutonomousCar

This repository contains all material needed in order to build the
RpiAutonomousCar used in Full Stack Embedded's 2017 workshops.

For more information about Full Stack Embedded, see
https://fullstackembedded.com.

## The hardware

The RpiAutonomousCar is a low-cost robotic car equipped with a Raspberry Pi for
logical control, interfaced to two servos, an ultrasonic sensor, an LED, and an
infrared sensor via a custom board. All components are mounted to a central
chassis with wheels attached to each motor and an additional wheel for
balancing.

## The software

The software consists of drivers for each component, an abstraction for the
entire robot, and three different high-level controllers. Each driver can be
used individually or through the robot abstraction. The high-level controllers
allow the robot to use its infrared sensor to follow a line on the ground and
use the ultrasonic sensor in order to drive autonomously. An additional
controller is included, which is a server-client application. The server runs
on the robot and translates commands sent by the client via a TCP/IP connection
into commands which control the physical robot.

## Where it's been used

This project has been built by the students of Full Stack Embedded during the
2017 workshop campaign in two schools: the Accra Institute of Technology and
Lome Business School.
