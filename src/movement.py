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
    kp = 0.56
    ki = 0.015
    kd = 0.38
    offset = 170
    targetPower = 200
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
        self.config()

    # sets black & white color before start
    def config(self):
        print("--> CONFIG")
        print("1. black")
        print("2. white")
        set_black = False
        set_white = False

        while not set_black:
            if self.button.value() == 1:
                self.black = self.scan()
                print(f"** set black: {self.black}")
                set_black = True
        time.sleep(1)
        while not set_white:
            if self.button.value() == 1:
                self.white = self.scan()
                print(f"** set black: {self.white}")
                set_white = True
        self.offset = (self.white + self.black) * 0.5
        print(f"** set offset: {self.offset}")
        print("Config done.")
        print("")
        time.sleep(3)

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
            return -1
        elif rgb_tuple[2] > rgb_tuple[0] + rgb_tuple[1]:
            return -2
        else:
            return rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2]

    # scans absolute parameter
    def scan_absolute(self):
        self.colorSensor.mode = 'RGB-RAW'
        rgb_tuple = self.colorSensor.bin_data("hhh")
        rgb_tuple = (int(0.8 * rgb_tuple[0]), int(0.25 * rgb_tuple[1]), int(0.8 * rgb_tuple[2]))

        if rgb_tuple[0] > 2 * (rgb_tuple[1] + rgb_tuple[2]):
            return "red"
        elif rgb_tuple[2] > rgb_tuple[0] + rgb_tuple[1]:
            return "blue"
        elif rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2] < 70:
            return "black"
        elif rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2] > 250:
            return "white"
        else:
            return "other"

    # left motor movement
    def moveA(self, pl):
        self.leftMotor.speed_sp = pl
        self.leftMotor.command = "run-forever"

    # right motor movement
    def moveC(self, pr):
        self.rightMotor.speed_sp = pr
        self.rightMotor.command = "run-forever"

    # stops robot movement
    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    # test function for finding parameters
    def find_parameter_per_tick(self):
        i = 0
        while i < 1000:
            # colorValue = self.scan()
            error = 1 - self.offset
            self.integral = 0.67 * self.integral + error
            self.derivative = error - self.lastError
            turn = self.kp * error + self.ki * self.integral + self.kd * self.derivative
            powerLeft = self.targetPower - turn
            powerRight = self.targetPower + turn
            self.moveA(110)
            self.moveC(110)
            self.lastError = error
            i += 1
        print("test done")

    # 30 degree turn
    def turn_45(self):
        i = 0
        self.leftMotor.speed_sp = -70
        self.rightMotor.speed_sp = 65
        while i < 311:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.stop()

    # 90 degree turnaround
    def turn_90(self):
        i = 0
        self.leftMotor.speed_sp = 75
        self.rightMotor.speed_sp = -80
        while i < 630:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.stop()

    # 360 degree turnaround
    def turn_360(self):
        i = 0
        self.leftMotor.speed_sp = 90
        self.rightMotor.speed_sp = -90
        while i < 2530:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.stop()

    # central movement function - works with pid
    def follow_line(self):
        time.sleep(5)
        print("!!!!! End drive by pressing button !!!!!")
        while self.button.value() == 0:  # condition for scan done
            colorValue = self.scan()
            if colorValue == -1 or colorValue == -2:
                self.stop()
                self.node(colorValue)
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

    # scans node for paths
    def node(self, color):
        print("! FOUND NODE !")
        i = 0
        self.leftMotor.speed_sp = 80
        self.rightMotor.speed_sp = 80
        while self.scan() == color:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
        while i < 200:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.turn_45()
        time.sleep(1)
        k = self.count_path()
        self.stop()
        print(f"counted paths: {k}")

    def count_path(self):
        self.leftMotor.speed_sp = 75
        self.rightMotor.speed_sp = -80
        current = "white"
        k = 0
        i = 0
        while i < 4:
            j = 0
            while j < 630:
                self.leftMotor.command = "run-forever"
                self.rightMotor.command = "run-forever"
                new_scan = self.scan_absolute()
                if current != new_scan:
                    if current == "white":
                        k += 1
                    current = new_scan
            i += 1
        self.stop()
        return k