# !/usr/bin/env python3

import math


class Odometry:


    alpha = 0
    beta = 0
    s = 0


    def __init__(self):
        self.a = 12
        self.distance_per_tick = (math.pi * 5.6)/360
        self.distance = None
        #self.distance_per_tick = 0.015


    def calculate(self, positions, old_X, old_Y, old_Dir):

        print("----calculate coordinates----")
        print("old Coordinates: " + str(old_X) + ", " + str(old_Y))

        for p in positions:

            print("position 0 left :>>>>>." + str(p[0]) + ">>>>>>")
            print("position 1 right :>>>>>." + str(p[1]) + ">>>>>>")

            l_distance = p[0] * self.distance_per_tick
            r_distance = p[1] * self.distance_per_tick

            # calculate alpha & beta
            alpha = (r_distance - l_distance) / self.a
            print("alpha :......" + str(alpha) + "........")
            beta = alpha / 2

            if alpha == 0:
                self.distance = r_distance
            else:
                self.distance = ((r_distance + l_distance)/alpha) * math.sin(beta)

            # maybe radian()
            delta_X = math.sin(math.radians(old_Dir) + beta) * self.distance
            delta_Y = math.cos(math.radians(old_Dir) + beta) * self.distance

            print("deltaX, deltaY:....." + str(delta_X) + "," + str(delta_Y) + "..........")

            # maybe round()
            new_Dir = math.radians(old_Dir) - alpha
            new_X = old_X + delta_X
            new_Y = old_Y + delta_Y

            old_X = new_X
            old_Y = new_Y
            old_Dir = math.degrees(new_Dir)

        print("new Coordinates: " + str(old_X) + ", " + str(old_Y))
        return ((old_X, old_Y), old_Dir)

