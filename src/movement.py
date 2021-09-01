# !/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
from odometry import Odometry


class Movement:
    # components
    leftMotor = ev3.LargeMotor("outA")
    rightMotor = ev3.LargeMotor("outC")
    colorSensor = ev3.ColorSensor("in1")
    button = ev3.TouchSensor("in2")
    ultrasonicSensor = ev3.UltrasonicSensor("in4")
    led = ev3.Leds()
    speaker = ev3.Sound()

    # pid variables
    kp = 0.58
    ki = 0.015
    kd = 0.8
    targetPower = 195
    integral = 0
    lastError = 0
    derivative = 0

    def __init__(self):
        self.leftMotor.reset()
        self.leftMotor.stop_action = "brake"
        self.rightMotor.reset()
        self.rightMotor.stop_action = "brake"
        self.ultrasonicSensor.mode = "US-SI-CM"
        self.odometry = Odometry()
        self.data = []
        self.black = 30
        self.white = 290
        self.offset = 130
        self.color = 0
        self.asteroid = False
        self.config()

    # sets black & white color before start
    def config(self):
        # self.led.set_color('LEFT', 'AMBER')
        # self.led.set_color('RIGHT', 'AMBER')
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
                print(f"** set white: {self.white}")
                set_white = True
        self.offset = (self.white + self.black) * 0.5
        print(f"** set offset: {self.offset}")
        print("Config done.")
        print("")
        time.sleep(3)

    # scans important parameter
    def scan(self):
        self.colorSensor.mode = 'RGB-RAW'
        rgb_tuple = self.colorSensor.bin_data("hhh")
        rgb_tuple = (int(0.8 * rgb_tuple[0]), int(0.25 * rgb_tuple[1]), int(0.8 * rgb_tuple[2]))

        if rgb_tuple[0] > 2 * (rgb_tuple[1] + rgb_tuple[2]):
            return -1
        elif rgb_tuple[2] > 1.25 * (rgb_tuple[0] + rgb_tuple[1]):
            return -2
        else:
            return rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2]

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

    # scans absolute parameter
    def scan_absolute(self):
        self.colorSensor.mode = 'RGB-RAW'
        rgb_tuple = self.colorSensor.bin_data("hhh")
        rgb_tuple = (int(0.8 * rgb_tuple[0]), int(0.25 * rgb_tuple[1]), int(0.8 * rgb_tuple[2]))

        if rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2] > 250:
            return "white"
        elif rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2] < 70:
            return "black"
        elif rgb_tuple[2] > 1.25 * (rgb_tuple[0] + rgb_tuple[1]):
            return "blue"
        elif rgb_tuple[0] > 2 * (rgb_tuple[1] + rgb_tuple[2]):
            return "red"
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
        self.leftMotor.speed_sp = 95
        self.rightMotor.speed_sp = -100
        while i < 350:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.stop()

    # 180 degree turnaround
    def turn_180(self):
        i = 0
        self.leftMotor.speed_sp = 95
        self.rightMotor.speed_sp = -100
        while i < 700:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.stop()

    # 270 degree turnaround
    def turn_270(self):
        i = 0
        self.leftMotor.speed_sp = 95
        self.rightMotor.speed_sp = -100
        while i < 1890:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.stop()

    # 360 degree turnaround
    def turn_360(self):
        i = 0
        self.leftMotor.speed_sp = 95
        self.rightMotor.speed_sp = -100
        while i < 2530:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.stop()

    # measure distance
    def distance(self):
        d = self.ultrasonicSensor.distance_centimeters
        if d < 8:
            self.stop()
            print("! FOUND ASTEROID !")
            self.speaker.beep()
            time.sleep(1)
            self.asteroid = True
            self.next_path(0, 90)

    # counts paths of a node
    def count_path(self):
        self.leftMotor.speed_sp = 75
        self.rightMotor.speed_sp = -80
        path = []
        i = 0
        while i < 4:
            j = 0
            found = False
            while j < 177:
                self.leftMotor.command = "run-forever"
                self.rightMotor.command = "run-forever"
                new_scan = self.scan_absolute()
                if new_scan == "black":
                    found = True
                j += 1
            if found:
                path.append(i * 90)
            i += 1
        self.stop()
        return path

    # central movement function - works with pid
    def follow_line(self):
        prevLeft = 0
        prevRight = 0
        time.sleep(2)
        self.data = []  # clearing odometry
        print("note: end drive by pressing button")
        while self.button.value() == 0:  # condition for scan done
            self.distance()
            colorValue = self.scan()
            if colorValue == -1 or colorValue == -2:
                self.stop()
                self.color = colorValue
                self.to_node()
                break
            else:
                error = colorValue - self.offset
                self.integral = 0.67 * self.integral + error
                self.derivative = error - self.lastError
                turn = self.kp * error + self.ki * self.integral + self.kd * self.derivative
                powerLeft = self.targetPower - turn
                powerRight = self.targetPower + turn
                newLeft = self.leftMotor.position
                newRight = self.rightMotor.position
                self.data.append((newLeft - prevLeft, newRight - prevRight))
                prevLeft = newLeft
                prevRight = newRight
                self.moveA(powerLeft)
                self.moveC(powerRight)
                self.lastError = error
        print("drive stopped.")

    # moves robot above node
    def to_node(self):
        if self.color == -1:
            print("! FOUND RED NODE !")
        elif self.color == -2:
            print("! FOUND BLUE NODE !")
        i = 0
        self.leftMotor.speed_sp = 80
        self.rightMotor.speed_sp = 80
        while self.scan() == self.color:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
        while i < 195:
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
            i += 1
        self.turn_45()
        time.sleep(1)

    # scans node for paths
    def node(self):
        k = self.count_path()
        self.stop()
        print(f"counted paths: {k}")
        return k

    # find next path
    def next_path(self, curDir, newDir):
        degree = (curDir + newDir) % 360  # HERE: which path to choose, in degree!
        if degree == 90:
            self.turn_90()
        elif degree == 180:
            self.turn_180()
        elif degree == 270:
            self.turn_270()
        else:
            self.leftMotor.speed_sp = 95
            self.rightMotor.speed_sp = -100
        while self.scan_absolute() != "black":
            self.leftMotor.command = "run-forever"
            self.rightMotor.command = "run-forever"
        self.stop()
