# !/usr/bin/env python3
import ev3dev.ev3 as ev3
import time


class Movement:
    # components
    leftMotor = ev3.LargeMotor("outA")
    rightMotor = ev3.LargeMotor("outC")
    colorSensor = ev3.ColorSensor("in1")
    button = ev3.TouchSensor("in2")
    # ultrasonicSensor = ev3.UltrasonicSensor("in3")

    # pid variables
    kp = 0.85
    ki = 0
    kd = 0
    offset = 170
    targetPower = 150
    integral = 0
    lastError = 0
    derivative = 0

    # config colors
    black = 50
    white = 330

    def __init__(self):
        self.leftMotor.reset()
        self.leftMotor.stop_action = "brake"
        self.rightMotor.reset()
        self.rightMotor.stop_action = "brake"

    # scans everything, for test
    def scan_detailed(self):
        active = False
        while not active:
            if self.button.value() == 1:
                self.colorSensor.mode = 'COL-COLOR'
                simple = self.colorSensor.value()
                if simple == 2:
                    simple_name = "blue"
                elif simple == 5:
                    simple_name = "red"
                elif simple == 6:
                    simple_name = "white"
                elif simple == 1:
                    simple_name = "black"
                else:
                    simple_name = "other"
                print(f"simple: {simple_name}")
                self.colorSensor.mode = 'RGB-RAW'
                rgb_tuple = self.colorSensor.bin_data("hhh")
                rgb_tuple = (rgb_tuple[0], int(0.25 * rgb_tuple[1]), rgb_tuple[2])
                print(f"rgb-tuple: {rgb_tuple}")
                rgb = rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2]
                print(f"rgb: {rgb}")
                time.sleep(2)

    # scans important parameter
    def scan(self):
        self.colorSensor.mode = 'RGB-RAW'
        rgb_tuple = self.colorSensor.bin_data("hhh")
        rgb_tuple = (int(0.8 * rgb_tuple[0]), int(0.25 * rgb_tuple[1]), int(0.8 * rgb_tuple[2]))

        if rgb_tuple[0] > 2 * (rgb_tuple[1] + rgb_tuple[2]):
            return "red"
        elif rgb_tuple[2] > rgb_tuple[0] + rgb_tuple[1]:
            return "blue"
        else:
            return rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2]

    # sets black & white color before start
    def config(self):
        print("--------------- CONFIG ---------------")
        print("1. black")
        print("2. white")
        set_black = False
        set_white = False

        while not set_black:
            if self.button.value() == 1:
                self.black = self.scan()
                print(f"** set BLACK: {self.black}")
                # self.black = self.black[0] + self.black[1] + self.black[2]
                # print("Converted BLACK: " + str(self.black))
                set_black = True
        time.sleep(3)
        while not set_white:
            if self.button.value() == 1:
                self.white = self.scan()
                print(f"** set WHITE: {self.white}")
                # self.white = self.white[0] + self.white[1] + self.white[2]
                # print("Converted WHITE: " + str(self.white))
                set_white = True
        self.offset = (self.white + self.black) * 0.5
        print(f"** set OFFSET: {self.offset}")
        print("Config done.")
        print("--------------------------------------")
        time.sleep(3)

    # left motor
    def moveA(self, pl):
        self.leftMotor.speed_sp = pl
        self.leftMotor.command = "run-forever"

    # right motor
    def moveC(self, pr):
        self.rightMotor.speed_sp = pr
        self.rightMotor.command = "run-forever"

    def find_distance_per_tick(self):
        i = 0
        while i < 1000:
            self.leftMotor.speed_sp = 40
            self.leftMotor.command = "run-forever"
            self.rightMotor.speed_sp = 40
            self.rightMotor.command = "run-forever"
        print("test done")

    # stops robot movement
    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    # 90 degree turnaround
    def turn_90(self):
        i = 0
        while i < 1000:
            self.leftMotor.speed_sp = 40
            self.leftMotor.command = "run-forever"
            self.rightMotor.speed_sp = -40
            self.rightMotor.command = "run-forever"
            i += 1

    # central movement function - works with pid
    def follow_line(self):
        time.sleep(5)
        print("!!!!! End drive by pressing button !!!!!")
        while self.button.value() == 0:
            colorValue = self.scan()
            if colorValue == "red" or colorValue == "blue":
                time.sleep(1)
                self.stop()
                break
            else:
                error = colorValue - self.offset
                self.integral = 0.67 * self.integral + error
                self.derivative = error - self.lastError
                turn = self.kp * error + self.ki * self.integral + self.kd * self.derivative
                print(f"__turn: {turn}")
                powerLeft = self.targetPower - turn
                powerRight = self.targetPower + turn
                self.moveA(powerLeft)
                self.moveC(powerRight)
                self.lastError = error

        print("Drive stopped.")
