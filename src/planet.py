#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import List, Tuple, Dict, Union


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

    paths = {}

    def __init__(self):
        """ Initializes the data structure """
        self.target = None

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
            # self.paths[target[0]][target[1]] = (start[0], start[1], weight)
        else:
            self.paths[start[0]] = {start[1]: (target[0], target[1], weight)}
            self.add_path(target, start, weight)
            # self.paths[target[0]] = {target[1]: (start[0], start[1], weight)}

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


    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[None, List[Tuple[Tuple[int, int], Direction]]]:
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

        shortest_path = []
        currentNode = start  #direction need to be added

        while currentNode != target:
            shortest_path.add(currentNode)  #direction need to be added
            possiblePaths = self.get_paths()[currentNode]
            nextnode = min(possiblePaths.values(), key=lambda t: t[2])[0]

            #in order to avoid any loop
            #if the next node = the current node -> search for another target node

            if nextnode in shortest_path:
                possiblePaths.pop(nextnode)
                nextnode = min(possiblePaths.values(), key=lambda t: t[2])[0]


            currentNode = nextnode   #direction need to be added

        return shortest_path
        pass
