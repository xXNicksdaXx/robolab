from planet import Planet, Direction
from communication import Communication
from odometry import Odometry
from movement import Movement


# from src.movement import Movement

class Robot:

    def __init__(self, communication):
        self.communication = communication
        self.planet = self.communication.planet
        self.odometry = Odometry()
        #self.communication = Communication()
        self.movement = Movement()
        self.data = None
        self.first_node = True


    def find_new_direction(self):

        print(f"coordinates1 : {self.planet.current_coordinates}")
        if self.first_node:
            print("ready")
            self.communication.send_ready()
            print("send ready")
            new_coordinates = self.planet.current_coordinates
            new_direction = self.planet.current_direction
            print("coordinates2, direction : ", self.planet.current_coordinates, self.planet.current_direction)
            self.first_node = False

        elif self.movement.asteroid:
            self.communication.send_path(self.planet.current_direction[0], self.planet.current_coordinates[1],
                                         int(self.planet.current_direction), self.planet.current_direction[0], self.planet.current_coordinates[1],
                                         int(self.planet.current_direction),
                                         "blocked")
            self.planet.found_obstacle()

        else:
            # calculate the new coordinates and direction
            a = self.odometry.calculate(self.data, self.planet.current_coordinates[0],
                                        self.planet.current_coordinates[1],
                                        int(self.planet.current_direction))
            new_coordinates = a[0]
            new_direction = Direction(a[1])
            print(f"a_odometry : {a}")
            self.communication.send_path(self.planet.current_coordinates[0], self.planet.current_coordinates[1],
                                         int(self.planet.current_direction), new_coordinates[0], new_coordinates[1],
                                         int(self.planet.get_end_dir(new_direction)), "free")
            self.planet.set_coordinastes(new_coordinates[0], new_coordinates[1])
            self.planet.current_direction = new_direction


        # beginn the exploration in class planet
        E = self.planet.explor()
        print(E)
        # if new node
        if E == "node not explored yet!":
            directions = self.movement.node()  # [int]
            self.planet.new_explored_node(directions)  #save in the dict
            print(f"exploredNodes : {self.planet.exploredNodes}")


        print(f"coordinates : {self.planet.current_coordinates}")

        next_direction = self.planet.chose_direction()
        print("next Direction: ", next_direction)
        self.planet.set_new_direction(next_direction)
        # path select
        self.communication.send_pathSelect(self.planet.current_coordinates[0], self.planet.current_coordinates[1],
                                           int(next_direction))
        print("direction from MS: ", self.planet.new_direction)
        return self.planet.new_direction



    def finished(self):
        for e in self.planet.exploredNodes.values():
            for d in e:
                if d[1] > 0:
                    return False
        return True

    # maybe needed
    def update_dir(self, new_direction):
        self.planet.update_path_Priority(self.planet.current_coordinates, new_direction, 0)

    def go_to_target(self, start, target):
        myList = self.planet.shortest_path(start, target)
        for l in myList:
            self.movement.next_path(l[1])
            # follow_line to the next node

    def prototyp(self):

        self.communication.send_test_planet()

        # while not finished:
        while True:

            self.movement.follow_line()
            # traget Messege -> shortest path
            # implement if we have a target -> do go_to_target
            self.data = self.movement.data

            self.find_new_direction()
            print(f"new Direction : {self.planet.new_direction}")

            #self.update_dir(new_Dir)

            # d = (int(self.current_direction) + int(new_Dir)) % 360
            self.movement.next_path(int(self.planet.current_direction), int(self.planet.new_direction))

        # <complit()
        #self.communication.send_complete(True)
