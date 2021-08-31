from src.planet import Planet, Direction
from src.communication import Communication
from src.odometry import Odometry
#from src.movement import Movement

class prototyp_actions_class:

    def __init__(self):
        planet = Planet()
        odometry = Odometry()
        communication = Communication()
        #movement = Movement()
        current_coordinats = None
        current_direction = None

    def get_start_paramenters(self):
        #.......self.communication.get_ready_messege()......
         pass

    def find_Node(self):

        a = self.odometry.calculate()
        new_coordinates = a[0]
        new_direction = a[1]

        self.planet.add_path((self.current_coordinats, self.current_direction), (new_coordinates, new_direction))

        if new_coordinates not in self.planet.exploredNodes:
            directions = self.movement.scan()  #i need hier a list of all possible path at the current node
            self.planet.addExploredNode(new_coordinates, directions)

        self.current_coordinats = new_coordinates
        self.current_direction = new_direction

        self.planet.update_path_Priority(self.current_coordinats, self.current_direction, 0)

        new_direction = self.planet.explor()
        #..........self.communication.send_path_messege().........
        #after the Muthership accepted the request of a new direction
        self.current_direction = new_direction

        self.planet.update_path_Priority(self.current_coordinats, self.current_direction, 0)

    def find_obstacle(self):

        self.planet.update_path_Priority(self.current_coordinats, self.current_direction, -1)

        # turn 360 dgree and return to the node befor
        #after return change the current dircetion
        self.current_direction = Direction((int(self.current_direction) + 180) % 360)






