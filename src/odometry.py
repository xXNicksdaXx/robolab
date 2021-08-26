# !/usr/bin/env python3
import ev3dev.ev3 as ev3
import time


class Odometry:
    leftMotor = ev3.LargeMotor("outA")
    rightMotor = ev3.LargeMotor("outC")
    colorSensor = ev3.ColorSensor("in1")
    colorSensor.mode = 'RGB-RAW'
    button = ev3.TouchSensor("in2")
    ultrasonicSensor = ev3.UltrasonicSensor("in3")

    con_p = 10
    con_i = 0
    con_d = 0
    offset = 45
    targetPower = 40
    integral = 0
    lastError = 0
    derivative = 0

    lightValue = 0
    black = 0
    white = 0


    def __init__(self):
        """
        Initializes odometry module
        """

        # YOUR CODE FOLLOWS (remove pass, please!)

    def config(self):
        print("----- CONFIG -----")
        print("1. set black")
        print("2. set white")
        set_black = False
        set_white = False

        while set_black == False:
            if Odometry.button.value() == 1:
                Odometry.black = Odometry.colorSensor.bin_data("hhh")
                print("Set BLACK: " + str(Odometry.black))
                Odometry.black = Odometry.black[0] + Odometry.black[1] + Odometry.black[2]
                print("Converted BLACK: " + str(Odometry.black))
                set_black = True

        time.sleep(5)

        while set_white == False:
            if Odometry.button.value() == 1:
                Odometry.white = Odometry.colorSensor.bin_data("hhh")
                print("Set WHITE: " + str(Odometry.white))
                Odometry.white = Odometry.white[0] + Odometry.white[1] + Odometry.white[2]
                print("Converted WHITE: " + str(Odometry.white))
                set_white = True

        Odometry.offset = Odometry.white - Odometry.black
        print("Set OFFSET: " + str(Odometry.offset))
        print("Config done.")


    def move(self):
        print("End drive by pressing button.")
        while Odometry.button.value() == 0:
            x = 0
        print("Drive stopped.")






