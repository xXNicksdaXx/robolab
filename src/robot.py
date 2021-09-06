from planet import Planet, Direction
from communication import Communication
from odometry import Odometry
from movement import Movement
import time



# from src.movement import Movement

class Robot:

    def __init__(self, communication):
        self.communication = communication
        self.planet = self.communication.planet
        self.odometry = Odometry()
        self.movement = Movement()
        self.data = None
        self.first_node = True


    def on_node(self):

        self.planet.delete_explored_path(self.planet.current_coordinates, self.planet.current_direction)
        print("paths_to_be_explored after delete : ", self.planet.paths_to_be_explored)

        if self.first_node:
            print("---first node---")
            self.communication.send_ready()
            self.first_node = False

        elif self.movement.asteroid:
            self.movement.asteroid = False
            self.communication.send_path(self.planet.current_coordinates[0], self.planet.current_coordinates[1],
                                         int(self.planet.current_direction), self.planet.current_coordinates[0],
                                         self.planet.current_coordinates[1], int(self.planet.current_direction),
                                         "blocked")

        else:
            # calculate the new coordinates and direction
            print(f"GIVEN PARAMETERS FOR ODOMETRY: current coordinates: {self.planet.current_coordinates}; current direction: {self.planet.current_direction}")
            a = self.odometry.calculate(self.data, self.planet.current_coordinates[0],
                                        self.planet.current_coordinates[1], int(self.planet.current_direction))
            new_coordinates = a[0]
            new_direction = Direction(a[1])
            self.communication.send_path(self.planet.current_coordinates[0], self.planet.current_coordinates[1],
                                         int(self.planet.current_direction), new_coordinates[0], new_coordinates[1],
                                         int(self.planet.get_end_dir(new_direction)), "free")

            self.planet.set_coordinates(new_coordinates[0], new_coordinates[1])
            self.planet.current_direction = new_direction
            print("current_coor, current_dir :", self.planet.current_coordinates, self.planet.current_direction)



    def find_new_direction(self):

        if self.planet.current_coordinates not in self.planet.visitedNodes:
            directions = self.movement.node()  # [int]
            self.planet.add_visited_node(self.planet.current_coordinates)
            print("visitedNodes : ", self.planet.visitedNodes)
            self.planet.delete_unvisited_node(self.planet.current_coordinates)
            print("unvisitedNodes : ", self.planet.unvisitedNodes)
            # self.planet.target_reached()
            print("target List :", self.planet.target)
            self.planet.add_path_to_be_explored(self.planet.current_coordinates, directions)
            self.planet.delete_explored_path(self.planet.current_coordinates, self.planet.get_end_dir(self.planet.current_direction))
            print("paths_to_be_explored : ", self.planet.paths_to_be_explored)

        self.planet.update_paths_to_be_explored(self.planet.current_coordinates, self.planet.current_direction, "free")
        next_direction = self.planet.find_next_direction()
        print("next_dir :", next_direction)
        if next_direction is None:
            return 0
        self.planet.set_new_direction(int(next_direction))
        # path select
        self.communication.send_pathSelect(self.planet.current_coordinates[0], self.planet.current_coordinates[1],
                                           int(next_direction))
        self.planet.check_direction(next_direction)

        return 1



    def prototype(self):

        self.communication.send_test_planet()

        while (not self.planet.exploration_complete() and not self.planet.target_reached()) or self.first_node :

            self.movement.follow_line()
            self.data = self.movement.data
            self.on_node()
            time.sleep(4)
            # if self.planet.target_reached():
            #     break
            i = self.find_new_direction()
            if i == 0:
                break
            time.sleep(4)
            print("after correcting currentDir: ", self.planet.current_direction, "NewDir : ",
                  self.planet.new_direction)
            self.movement.next_path(int(self.planet.current_direction), int(self.planet.new_direction))
            self.planet.current_direction = self.planet.new_direction
            print("exploration ", self.planet.exploration_complete())
            print("target :", self.planet.all_targets_reached())
            print("first node: ", self.first_node)

        # complit()

        print("end Exploration")
        self.communication.send_complete(not self.planet.target_reached())

