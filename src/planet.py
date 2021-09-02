#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import List, Tuple, Dict, Union
import math


# from communication import Communication


@unique
class Direction(IntEnum):
    """ Directions in shortcut """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


Weight = int
"""
Weight of a given path (received from the server)

Value:  -1 if blocked path
        >0 for all other paths
        never 0
"""


class Planet:
    """
    Contains the representation of the map and provides certain functions to manipulate or extend
    it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None
        self.paths = {}
        self.exploredNodes = {}
        self.current_coordinates = None
        self.current_direction = None
        self.new_direction = None
        self.finished = False

    # some methods wich are related to communication
    def set_parameter(self, startX, startY, startDir):
        self.current_coordinates = (startX, startY)
        self.current_direction = startDir

    def set_new_direction(self, new_direction):
        print("set the new direction")
        self.new_direction = Direction(new_direction)

    def set_coordinastes(self, X, Y):
        self.current_coordinates = (X, Y)

    def set_traget(self, targetX, targetY):
        self.target = (targetX, targetY)

    def get_end_dir(self, dir):
        return Direction((int(dir) + 180) % 360)

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it

        Example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """
        # YOUR CODE FOLLOWS (remove pass, please!)

        # if the Node is already discovered
        if start[0] in self.paths:
            # if the Path exist in the Dictionary
            if start[1] in self.paths[start[0]]:
                return 0
            self.paths[start[0]][start[1]] = (target[0], target[1], weight)
            self.add_path(target, start, weight)
        else:
            self.paths[start[0]] = {start[1]: (target[0], target[1], weight)}
            self.add_path(target, start, weight)

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """
        Returns all paths

        Example:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2),
                    Direction.WEST: ((0, 3), Direction.NORTH, 1)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """
        # YOUR CODE FOLLOWS (remove pass, please!)
        return self.paths

    # Method to find the MinDistance
    def findMinimum(self, list: [], dict: {}):

        myList = []
        for l in list:
            myList.append((l, dict[l]))
        Min = min(myList, key=lambda t: t[1])
        return Min[0]

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[
        None, List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes

        Examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: 2-Tuple[List, Direction]
        """

        # YOUR CODE FOLLOWS (remove pass, please!)

        # if the target Node is not in the Paths Dictionary
        if target not in self.paths:
            print("Target not reachable")
            return None

        # else if the target is reachable calculat Dijkstra and get the result path
        return self.dijkstra(start, target)

    def dijkstra(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[
        None, List[Tuple[Tuple[int, int], Direction]]]:

        # Initialization
        Q = []
        vertex = self.paths.keys()
        dist = {}
        prev = {}
        shortest_path = []
        shortest_path1 = []

        # all Nodes will get the weight Infinity
        for v in vertex:
            dist[v] = math.inf
            prev[v] = None
            Q.append(v)

        # Remove all blocked paths
        for q in Q:
            if dist[q] == -1:
                Q.remove(q)

        dist[start] = 0

        while Q:
            u = self.findMinimum(Q, dist)  # Node with minimum distance
            Q.remove(u)

            if u == target:
                break
            for p in self.paths[u].values():  # p = (Node, Dir, Weight)
                alt = dist[u] + p[2]
                if alt < dist[p[0]]:
                    dist[p[0]] = alt

                    Dir = Direction.NORTH
                    for n in self.paths[u]:
                        if self.paths[u][n] == p:
                            Dir = n
                    prev[p[0]] = (u, Dir)

        uTraget = target
        if prev[uTraget] or uTraget == start:
            while prev[uTraget]:
                shortest_path.append(prev[uTraget])
                uTraget = prev[uTraget][0]

        while shortest_path:  # to fix the order of the first list using lifo order
            shortest_path1.append(shortest_path.pop())

        return shortest_path1

    # --------------------for the intelligent Exploration:---------------------------

    # for add new explored node:
    # transforming the directions from int to Direction
    def get_real_directions(self, directions: List[int], current_dir):
        real_dir = []
        for d in directions:
            real_dir.append(Direction((int(current_dir) + d) % 360))
        return real_dir

    # set for every direction Priority
    def setPriorityList(self, direction: List[Direction]):
        prioDir = []
        for d in direction:
            if d == Direction.NORTH:
                prioDir.append((d, 4))
            elif d == Direction.SOUTH:
                prioDir.append((d, 1))
            elif d == Direction.WEST:
                prioDir.append((d, 2))
            else:
                prioDir.append((d, 3))

        return prioDir

    def addExploredNode(self, node: Tuple[int, int], directions: List[int], current_dir):
        # dircetions = [0,90,180,270]
        real_dir = self.get_real_directions(directions, current_dir)
        prioDir = self.setPriorityList(real_dir)
        self.exploredNodes[node] = prioDir

    # ------------for the main exploration ---------------

    def update_path_Priority(self, node: Tuple[int, int], direction: Direction, priority: int):
        for a in self.exploredNodes[node]:
            if a[0] == direction:
                self.exploredNodes[node].remove(a)
                self.exploredNodes[node].append((direction, priority))

    # chosing the direction with the hieghest priority
    def chose_direction(self):
        bestPriority = max(self.exploredNodes[self.current_coordinates], key=lambda t: t[1])
        return bestPriority[0]

    def found_obstacle(self):
        self.update_path_Priority(self.current_coordinates, self.current_direction, -1)

        # after return 360 degree change the current dircetion
        self.current_direction = Direction((int(self.current_direction) + 180) % 360)

    def explor(self):

        if self.current_coordinates not in self.exploredNodes:
            return "node not explored yet!"

        # if the node is explored change the priority of the path
        self.update_path_Priority(self.current_coordinates, self.get_end_dir(self.current_direction), 0)

    def new_explored_node(self, directions):
        self.addExploredNode(self.current_coordinates, directions, self.current_direction)

    # def get_next_direction(self, current_coordinates):
    #     self.new_direction = self.chose_direction()
    #     # commmunication.send_pathSelect(current_coordinates[0], current_coordinates[1], direction)
    #     return self.new_direction
