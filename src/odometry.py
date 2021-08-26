# !/usr/bin/env python3
import ev3dev.ev3 as ev3
import time


class Odometry:
    # components
    leftMotor = ev3.LargeMotor("outA")
    rightMotor = ev3.LargeMotor("outC")
    colorSensor = ev3.ColorSensor("in1")
    button = ev3.TouchSensor("in2")
    ultrasonicSensor = ev3.UltrasonicSensor("in3")

    # pid variables
    kp = 0.8
    ki = 0
    kd = 0
    offset = 0
    targetPower = 250
    integral = 0
    lastError = 0
    derivative = 0

    # config colors
    black = 0
    white = 0

    def __init__(self):
        """
        Initializes odometry module
        """

    def scan_detailed(self):
        self.colorSensor.mode = 'COL-COLOR'
        simple = self.colorSensor.value()
        print(f"simple: {simple}")
        self.colorSensor.mode = 'COL-REFLECT'
        reflect = self.colorSensor.value()
        print(f"reflect: {reflect}")
        self.colorSensor.mode = 'RGB-RAW'
        rgb = self.colorSensor.value()
        print(f"rgb: {rgb}")
        rgb_tuple = self.colorSensor.bin_data("hhh")
        print(f"rgb-tuple: {rgb_tuple}")
        c_tuple = (simple, reflect, rgb, rgb_tuple)
        print(f"tuple: {c_tuple}")
        return c_tuple

    def scan_fast(self):
        self.colorSensor.mode = 'COL-REFLECT'
        return self.colorSensor.value()

    # sets black & white color before start
    def config(self):
        print("----- CONFIG -----")
        print("1. set black")
        print("2. set white")
        set_black = False
        set_white = False

        while not set_black:
            if self.button.value() == 1:
                scan = self.scan_detailed()
                self.black = scan[1]
                print("Set BLACK: " + str(self.black))
                # self.black = self.black[0] + self.black[1] + self.black[2]
                # print("Converted BLACK: " + str(self.black))
                set_black = True
        time.sleep(3)
        while not set_white:
            if self.button.value() == 1:
                scan = self.scan_detailed()
                self.white = scan[1]
                print("Set WHITE: " + str(self.white))
                # self.white = self.white[0] + self.white[1] + self.white[2]
                # print("Converted WHITE: " + str(self.white))
                set_white = True
        time.sleep(3)
        self.offset = (self.white + self.black) * 0.5
        print("Set OFFSET: " + str(self.offset))
        print("Config done.")
        time.sleep(3)
        print("------------------")

    # left motor
    def moveA(self, pl):
        self.leftMotor.stop_action = "brake"
        self.leftMotor.speed_sp = pl
        self.leftMotor.command = "run-forever"

    # right motor
    def moveC(self, pr):
        self.rightMotor.stop_action = "brake"
        self.rightMotor.speed_sp = pr
        self.rightMotor.command = "run-forever"

    # central movement function - works with pid
    def pid(self):
        print("!!!!! End drive by pressing button !!!!!")
        while self.button.value() == 0:
            colorValue = self.colorSensor.value()
            error = colorValue - self.offset
            self.integral = 0.67 * self.integral + error
            self.derivative = error - self.lastError
            turn = self.kp * error + self.ki * self.integral + self.kd * self.derivative
            powerLeft = self.targetPower + turn
            powerRight = self.targetPower - turn
            self.moveA(powerLeft)
            self.moveC(powerRight)
            self.lastError = error

        print("Drive stopped.")