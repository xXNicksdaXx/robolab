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
        self.visitedNodes = []
        self.unvisitedNodes = []
        self.paths_to_be_explored = []
        self.current_coordinates = None
        self.current_direction = None
        self.new_direction = None
        self.finished = False

    # some methods wich are related to communication
    def set_parameter(self, startX, startY, startDir):
        self.current_coordinates = (startX, startY)
        self.current_direction = Direction(startDir)

    def set_new_direction(self, new_direction):
        self.new_direction = Direction(new_direction)

    def set_coordinates(self, X, Y):
        self.current_coordinates = (X, Y)

    def set_target(self, targetX, targetY):
        self.target = (targetX, targetY)

    def get_end_dir(self, direction):
        return Direction((int(direction) + 180) % 360)

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
                self.paths[start[0]][start[1]] = (target[0], target[1], weight)
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
    def find_minimum(self, list: [], dict: {}):

        myList = []
        for element in list:
            myList.append((element, dict[element]))
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

        # if the target Node is not in the Paths Dictionary
        if target not in self.paths:
            return None

        # else if the target is reachable calculate Dijkstra and get the result path
        return self.dijkstra(start, target)[0]

    def dijkstra(self, start: Tuple[int, int], target: Tuple[int, int]):
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
            u = self.find_minimum(Q, dist)  # Node with minimum distance
            Q.remove(u)

            if u == target:
                break
            for p in self.paths[u].values():  # p = (Node, Dir, Weight)
                if p[0] != u and p[2] != -1:
                    alt = dist[u] + p[2]
                    if alt < dist[p[0]]:
                        dist[p[0]] = alt

                        Dir = Direction.NORTH
                        for n in self.paths[u]:
                            if self.paths[u][n] == p:
                                Dir = n
                        prev[p[0]] = (u, Dir)
        d = 0
        u_target = target
        if prev[u_target] or u_target == start:
            while prev[u_target]:
                d += dist[u_target]
                shortest_path.append(prev[u_target])
                u_target = prev[u_target][0]

        while shortest_path:  # to fix the order of the first list using lifo order
            shortest_path1.append(shortest_path.pop())
        return shortest_path1, d

    # --------------------for the intelligent Exploration:---------------------------

    # for add new explored node:
    # transforming the directions from int to Direction
    def get_real_directions(self, directions: List[int]):
        real_dir = []
        for d in directions:
            real_dir.append(Direction((int(self.current_direction) + d) % 360))
        return real_dir

    def add_visited_node(self, node):
        self.visitedNodes.append(node)

    def add_unvisited_node(self, node):
        if node not in self.unvisitedNodes:
            self.unvisitedNodes.append(node)

    def delete_unvisited_node(self, node):
        if node in self.unvisitedNodes:
            self.unvisitedNodes.remove(node)

    def add_path_to_be_explored(self, node, directions):
        if node in self.get_paths():
            myList = self.get_paths()[node].keys()
        else:
            myList = []

        real_directions = self.get_real_directions(directions)
        L = len(real_directions) - 1
        # for i in range(0, L + 1):
        #     d = real_directions[L - i]
        #     if d not in myList:
        #       self.paths_to_be_explored.append((node, d))
        for d in real_directions:
            if d not in myList:
                self.paths_to_be_explored.append((node, d))

    def delete_explored_path(self, node, direction):
        if (node, direction) in self.paths_to_be_explored:
            self.paths_to_be_explored.remove((node, direction))

    def choose_closest_option(self):
        options = []
        if self.paths_to_be_explored:
            for node in self.paths_to_be_explored:
                if node[0] == self.current_coordinates:
                    return node[1]
            for node in self.paths_to_be_explored:
                path = self.dijkstra(self.current_coordinates, node[0])
                options.append(path)
        if self.unvisitedNodes:
            for node in self.unvisitedNodes:
                path = self.dijkstra(self.current_coordinates, node)
                options.append(path)
        better_options = [value for value in options if value != ([], 0)]
        if better_options:
            minimum = min(better_options, key=lambda t: t[1])[0][0][1]
            return minimum

    def find_next_direction(self):
        if self.target:
            sh_path = self.shortest_path(self.current_coordinates, self.target)
            if sh_path:
                return sh_path.pop(0)[1]

        if self.paths_to_be_explored or self.unvisitedNodes:
            best_tuple = self.choose_closest_option()
            return best_tuple

        return None

    def target_reached(self):
        return self.target == self.current_coordinates

    def all_targets_reached(self):
        return not self.target  # return [] -> True

    def exploration_complete(self):
        if not self.unvisitedNodes and not self.paths_to_be_explored:
            return True
        return False

    def update_paths_to_be_explored(self, node, direction, status):
        for tuple in self.paths_to_be_explored:
            if tuple == (node, direction):
                self.delete_explored_path(node, direction)

    def react_to_path_unveiled(self, node, direction, status):
        if node in self.visitedNodes:
            self.update_paths_to_be_explored(node, direction, status)
            return
        self.add_unvisited_node(node)
        if len(self.get_paths()[node].keys()) == 4:
            self.delete_unvisited_node(node)

    def check_direction(self, next_dir):
        if self.current_coordinates in self.get_paths():
            if self.new_direction in self.get_paths()[self.current_coordinates].keys():
                if self.get_paths()[self.current_coordinates][self.new_direction][2] == -1:
                    # if the path is already explored do not explore it again
                    self.new_direction = next_dir
