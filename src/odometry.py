# !/usr/bin/env python3

import math
class Odometry:
    def __init__(self):
        """
        Initializes odometry module
        """
        # YOUR CODE FOLLOWS (remove pass, please!)
        self.a = 10
        self.distane_per_tick = math.pi*5.6

    # def calculate_r(self, l_position, r_position):   #retrun the dr and dl
    #     r_distance = (r_position*self.distane_per_tick)/50
    #     l_distance = (l_position*self.distane_per_tick)/50
    #
    #     if r_distance == l_distance:
    #         r = r_distance
    #
    #     r = (self.a*l_distance)/(r_distance-l_distance)


    def calculate(self, positions, old_X, old_Y, old_Dir):

        print("----calculate coordinates----")
        print("old Coordinates: " + str(old_X) + ", " + str(old_Y))

        for p in positions:

            print("position 0 left :>>>>>."+str(p[0])+">>>>>>")
            print("position 1 right :>>>>>."+str(p[1])+">>>>>>")

            l_distance = p[0] * self.distane_per_tick
            r_distance = p[1] * self.distane_per_tick

            if r_distance == l_distance:
                r = r_distance
                print("Rd = Rl =   .....  "+str(r) + "......")
            else:
                r = (self.a * l_distance) / (r_distance - l_distance)

            #maybe rund(r)
            alpha = (l_distance - r_distance) / self.a
            print("alpha :......"+str(alpha)+"........")
            beta = alpha/2

            if alpha == 0:
                s = r
            else:
                s = (r_distance + l_distance)*((math.sin(math.radians(beta))/alpha))

            #maybe radian()
            delta_X = -math.sin(int(old_Dir) + beta) * s
            delta_Y = math.cos(int(old_Dir) + beta) * s

            print("deltaX, deltaY:....."+str(delta_X)+","+str(delta_Y)+"..........")

            #maybe rund()
            new_Dir = int(old_Dir) + alpha
            new_X = old_X + delta_X
            new_Y = old_Y + delta_Y

            old_X = new_X
            old_Y = new_Y
            old_Dir = math.degrees(new_Dir)

        print("new Coordinates: " + str(old_X) + ", " + str(old_Y))
        return ((old_X, old_Y), old_Dir)

        pass

