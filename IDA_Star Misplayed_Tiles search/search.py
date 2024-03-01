# CS 411 - Assignment 6 Starter Code
# IDA* Misplayed Tiles Search
# Name: Duc Tran, UIN: 679876782
# Spring 2024

import random
import math
import time
import psutil
import os
from collections import deque
from heapq import *
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action == 'L':
            if empty_index % self.size > 0:
                new_tiles[empty_index - 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index - 1]
        if action == 'R':
            if empty_index % self.size < (self.size - 1):
                new_tiles[empty_index + 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index + 1]
        if action == 'U':
            if empty_index - self.size >= 0:
                new_tiles[empty_index - self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index - self.size]
        if action == 'D':
            if empty_index + self.size < self.size * self.size:
                new_tiles[empty_index + self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index + self.size]
        return Board(new_tiles)


# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __lt__(self, other):
        return id(self)<= id(other)
    
    def __hash__(self):
        return hash(tuple(self.state.tiles))

class Search:

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None)

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        children = []
        actions = ['L', 'R', 'U', 'D']  # left,right, up , down ; actions define direction of movement of empty tile
        for action in actions:
            child_state = parent_node.state.execute_action(action)
            child_node = Node(child_state, parent_node, action)
            children.append(child_node)
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while (node.parent is not None):
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path
    
    # This function get the depth of any nodes by backtracking and counting the number of parents
    def get_depth(self, node):
        depth = 0
        while (node.parent is not None):
            depth += 1
            node = node.parent
        return depth
            
    
    # This function get all the misplay tiles between original states and the current node states excluding blank (number 0)
    def get_difference(self, cur_tiles):
        difference = 0
        goal_states = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
        for i in range(0, 16):
            if goal_states[i] != cur_tiles[i] and cur_tiles[i] != '0':
                difference += 1
        return difference

    def IDA_star_search(self, root_node):
        bound_num = self.get_difference(root_node.state.tiles) + self.get_depth(root_node)
        path = None
        while path == None:
            path, num_node, time, memory, bound_num = self.A_star_misplayed_tiles(root_node, bound_num)
        return path, num_node, time, memory


    # This function run A* for the A* misplayed_titles as h function
    # The g function is the depth funcion, with each depth cost 1
    # f(A*) = g(depth) + h(misplayed_titles)
    def A_star_misplayed_tiles(self, root_node, bound):
        start_time = time.time()
        frontier = []
        max_memory = 0
        explored = set()
        heappush(frontier, (self.get_difference(root_node.state.tiles) + self.get_depth(root_node) , root_node))
        while (len(frontier) > 0):
            max_memory = max(max_memory, sys.getsizeof(frontier) + sys.getsizeof(explored))
            cur_node = heappop(frontier)[1]
            explored.add(cur_node)

            # Prune all the child that greater than bound
            if (self.get_difference(cur_node.state.tiles) + self.get_depth(cur_node)) > bound:
                continue
            
            # Return goal if found
            if (self.goal_test(cur_node.state.tiles)):
                path = self.find_path(cur_node)
                end_time = time.time()
                return path, len(explored), (end_time - start_time), max_memory, new_bound
            
            # Set new_bound to infinite
            new_bound = float('inf')
            
            # Getting new bound as well as pushing child that is less than bound
            for child in self.get_children(cur_node):
                if child not in explored:
                    heappush(frontier, (self.get_difference(child.state.tiles) + self.get_depth(child), child))
                    if self.get_difference(child.state.tiles) + self.get_depth(child) < new_bound:
                        new_bound = self.get_difference(child.state.tiles) + self.get_depth(child)
        return None, None, None, None, new_bound
    

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def solve(self, input):
        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.IDA_star_search(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

if __name__ == '__main__':
    agent = Search()
    agent.solve("1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12")