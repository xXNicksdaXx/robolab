from src.planet import Planet, Direction
from src.communication import Communication
from src.odometry import Odometry
from src.movement import Movement
#from src.movement import Movement

class prototyp_actions_class:

    def __init__(self):
        self.planet = Planet()
        self.odometry = Odometry()
        self.communication = Communication()
        self.movement = Movement()
        self.current_coordinats = None
        self.current_direction = None
        self.data = None

    def get_start_paramenters(self):
        #.......self.communication.get_ready_messege()......
         pass

    def find_Node(self):


        a = self.odometry.calculate(self.data, self.current_coordinats[0], self.current_coordinats[1], self.current_direction)
        new_coordinates = a[0]
        new_direction = a[1]

        if self.movement.bool:
            self.find_obstacle()
            self.movement.bool = False

        else:
            d = self.odometry.calculate_distance()
            self.planet.add_path((self.current_coordinats, self.current_direction), (new_coordinates, new_direction),d)

            if new_coordinates not in self.planet.exploredNodes:
                directions = self.movement.node()  #i need hier a list of all possible path at the current node
                self.planet.addExploredNode(new_coordinates, directions, self.current_direction)

            self.current_coordinats = new_coordinates
            self.current_direction = new_direction

            self.planet.update_path_Priority(self.current_coordinats, self.current_direction, 0)

            new_direction = self.planet.chose_direction(new_coordinates)
            return new_direction
        # #..........self.communication.send_path_messege().........
        # #after the Muthership accepted the request of a new direction
        # self.current_direction = new_direction
        #
        # self.planet.update_path_Priority(self.current_coordinats, self.current_direction, 0)

    def find_obstacle(self):

        self.planet.update_path_Priority(self.current_coordinats, self.current_direction, -1)

        # turn 360 dgree and return to the node befor
        #after return change the current dircetion
        self.current_direction = Direction((int(self.current_direction) + 180) % 360)


    def finished(self):
        pass

    def update_Dir(self, new_direction):
        self.current_direction = new_direction

        self.planet.update_path_Priority(self.current_coordinats, self.current_direction, 0)


    def prototyp(self):

        #while not finished:
        while True:
            self.movement.follow_line()     # self.data = self.movement.follow_line()


            self.find_Node()
            new_Dir = self.find_Node()
            #<<<<<communication >>>>
            self.update_dir(new_Dir)

            d = (self.current_direction + new_Dir) % 360
            self.movement.next_path(d)









