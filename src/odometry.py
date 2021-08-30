# !/usr/bin/env python3

import math


class Odometry:
    def __init__(self):
        self.a = 12
        # self.distance_per_tick = math.pi * 5.6
        self.distance_per_tick = 0.015

    def calculate(self, positions, old_X, old_Y, old_Dir):

        print("----calculate coordinates----")
        print("old Coordinates: " + str(old_X) + ", " + str(old_Y))

        old_Dir = math.radians(old_Dir)

        for p in positions:

            print("position 0 left :>>>>>." + str(p[0]) + ">>>>>>")
            print("position 1 right :>>>>>." + str(p[1]) + ">>>>>>")

            l_distance = p[0] * self.distance_per_tick
            r_distance = p[1] * self.distance_per_tick

            # calculate alpha & beta
            alpha = (l_distance - r_distance) / self.a
            print("alpha :......" + str(alpha) + "........")
            beta = alpha / 2

            if alpha == 0:
                s = r_distance
            else:
                s = (r_distance + l_distance)/alpha * math.sin(beta)

            # maybe radian()
            delta_X = -math.sin(math.radians(int(old_Dir)) + beta) * s
            delta_Y = math.cos(math.radians(int(old_Dir)) + beta) * s

            print("deltaX, deltaY:....." + str(delta_X) + "," + str(delta_Y) + "..........")

            # maybe round()
            new_Dir = math.radians(int(old_Dir)) + alpha
            new_X = old_X + delta_X
            new_Y = old_Y + delta_Y

            old_X = new_X
            old_Y = new_Y
            old_Dir = new_Dir

        print("new Coordinates: " + str(old_X) + ", " + str(old_Y))
        return ((old_X, old_Y), math.degrees(old_Dir))

