# !/usr/bin/env python3
import ev3dev.ev3 as ev3


class Odometry:
    leftMotor = ev3.LargeMotor("outA")
    rightMotor = ev3.LargeMotor("outC")
    lightSensor = ev3.LightSensor()
    lightSensor.mode = 'RGB-RAW'
    button = ev3.TouchSensor()
    ultrasonicSensor = ev3.UltrasonicSensor()
    gyroSensor = ev3.GyroSensor()

    con_p = 10
    con_i = 0
    con_d = 0
    offset = 45
    target_power = 40
    integral = 0
    lastError = 0
    derivative = 0

    black = 0
    white = 0
    gyro = 0


    def __init__(self):
        """
        Initializes odometry module
        """

        # YOUR CODE FOLLOWS (remove pass, please!)

    def config(self):
        set_black = False
        set_white = False
        set_gyro = False

        while set_black == False:
            if Odometry.button.value() == 1:
                Odometry.black = Odometry.lightSensor.bin_data("hhh")
                print("Set BLACK: " + str(Odometry.black))
                set_black = True

        while set_white == False:
            if Odometry.button.value() == 1:
                Odometry.white = Odometry.lightSensor.bin_data("hhh")
                print("Set WHITE: " + str(Odometry.white))
                set_white = True

        offset = Odometry.white - Odometry.black

        while set_gyro == False:
            if Odometry.button.value() == 1:
                Odometry.gyro = Odometry.gyroSensor.value()
                print("Set GYRO: " + str(Odometry.gyro))
                set_gyro = True

        print("Config done.")


    def move(self):
        print("End drive by pressing button.")
        while Odometry.button.value() == 0:


        print("Drive stopped.")






