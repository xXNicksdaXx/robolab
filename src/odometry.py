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
        old_X *= 50
        old_Y *= 50

        for p in positions:
            l_distance = p[0] * self.distance_per_tick
            r_distance = p[1] * self.distance_per_tick

            # calculate alpha & beta
            alpha = (r_distance - l_distance) / self.a
            beta = alpha / 2

            if alpha == 0:
                self.distance = r_distance
            else:
                self.distance = ((r_distance + l_distance)/alpha) * math.sin(beta)

            # maybe radian()
            delta_X = -math.sin(math.radians(old_Dir) - beta) * self.distance
            delta_Y = math.cos(math.radians(old_Dir) + beta) * self.distance

            # maybe round()
            new_Dir = math.radians(old_Dir) - alpha
            new_X = old_X + delta_X
            new_Y = old_Y + delta_Y

            old_X = new_X
            old_Y = new_Y
            old_Dir = math.degrees(new_Dir)

        print(old_X)
        print(old_Y)
        print(old_Dir)
        print(self.distance)
        x = int(round(old_X / 50))
        y = int(round(old_Y / 50))
        dir = self.round_angle(old_Dir)

        return ((x, y), dir)

    # rounds angle
    def round_angle(self, angle):
        angle = int(round(angle+360)) % 360
        print(angle)
        if 70 < angle < 110:
            return 90
        elif 160 < angle < 200:
            return 180
        elif 250 < angle < 290:
            return 270
        elif 340 < angle < 360 or 0 <= angle < 20:
            return 0
        else:
            return "no valid angle"