import random
import logging
import math
import sympy as sp
from sympy.abc import x, h, k, theta
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from scipy.optimize import root as sci_root

l = logging.getLogger(__name__)


class MicroMouseMaze:
    """
    A class to represent and visualize a 2D maze for a micro mouse using a graph structure.
    
    Attributes:
    -----------
    size : int
        The size of one side of the square maze (default is 16).
    total_nodes : int
        The total number of nodes in the maze, calculated as size * size.
    maze : networkx.Graph
        The graph representing the maze, with nodes and edges defining the structure.
    visited_nodes : set
        A set to track visited nodes.
    """
    diagonal_path_eq = sp.Piecewise(
        (
            x**5 * 16,
            x < 0.5,
        ),
        (
            1 - ((-2 * x + 2)**5) / 2,
            True,
        ),
    )
    path_eq = sp.Piecewise(
        (
            diagonal_path_eq.subs(
                x,
                x - sp.Rational(5, 2),
            ),
            (x > 2.5) & (x < 3.5),
        ),
        (
            1 - diagonal_path_eq.subs(
                x,
                x - sp.Rational(7, 2),
            ),
            (3.5 < x) & (x < 4.5),
        ),
        (
            0,
            True,
        ),
    )

    line_eq = ((x - h) / sp.tan(theta + (sp.pi / 2))) + k

    def __init__(self, size=16):
        """
        Initializes the MicroMouseMaze class.
        
        Parameters:
        -----------
        size : int, optional
            The size of one side of the square maze (default is 16).
        """
        self.size = size
        self.total_nodes = size * size
        self.maze = nx.Graph()
        self.visited_nodes = set()
        self._initialize_maze()

    def _initialize_maze(self):
        """
        Initializes the maze structure by adding nodes to the graph.
        
        Each node represents a cell in the maze grid, numbered from 0 to (size * size - 1).
        """
        for node in range(self.total_nodes):
            self.maze.add_node(node)

    def visit_node(self, node):
        """
        Marks a specified node as visited.
        
        Parameters:
        -----------
        node : int
            The node to be marked as visited.
        """
        if 0 <= node < self.total_nodes:
            self.visited_nodes.add(node)

    def is_visited(self, node):
        """
        Checks if a specified node has been visited.
        
        Parameters:
        -----------
        node : int
            The node to check for visitation.
        
        Returns:
        --------
        bool
            True if the node has been visited, False otherwise.
        """
        return node in self.visited_nodes

    def add_edges(
        self,
        current_node,
        facing_direction='north',
        front=False,
        right=False,
        left=False,
        back=False,
        make_visited: bool = True,
    ):
        """
        Adds edges between the current node and its neighbors based on the given directional inputs, 
        adjusting them based on the current facing direction (north, east, south, or west).
        
        Parameters:
        -----------
        current_node : int
            The node from which edges are added.
        facing_direction : str, optional
            The direction the user is facing (north, east, south, or west).
        front : bool, optional
            True if there is an open path to the front (based on the current facing direction).
        right : bool, optional
            True if there is an open path to the right.
        left : bool, optional
            True if there is an open path to the left.
        back : bool, optional
            True if there is an open path to the back (based on the current facing direction).
        make_visited : bool, optional
            If True, marks the current node as visited (default is True).
        """

        #* NOTE: north is switched with south and east is switched with west in all the comments
        #* NOTE: north is switched with south and east is switched with west in all the comments
        #* NOTE: north is switched with south and east is switched with west in all the comments
        #* NOTE: north is switched with south and east is switched with west in all the comments
        #* NOTE: north is switched with south and east is switched with west in all the comments
        if make_visited:
            self.visit_node(current_node)

        if not (0 <= current_node < self.total_nodes):
            return  # Ensure the current node is valid

        # Define direction mappings based on the facing direction
        directions = ['south', 'west', 'north', 'east']
        facing_index = directions.index(facing_direction)

        # Rotate the directions based on the facing direction
        # For example, if facing east, then "front" becomes "east", "right" becomes "south", etc.
        rotated_directions = directions[
            facing_index:] + directions[:facing_index]

        # Now, map the front, right, left, and back to their new directions
        # front -> first in rotated_directions, right -> second, left -> third, back -> fourth
        front_direction = rotated_directions[0]
        right_direction = rotated_directions[1]
        left_direction = rotated_directions[3]
        back_direction = rotated_directions[2]

        # Calculate the row and column of the current node in the grid
        row, col = divmod(current_node, self.size)

        # Add edges based on the directional flags
        if front and front_direction == 'south' and row > 0:  # Node above (north)
            self.maze.add_edge(current_node, current_node - self.size)
        elif front and front_direction == 'west' and col < self.size - 1:  # Node to the right (east)
            self.maze.add_edge(current_node, current_node + 1)
        elif front and front_direction == 'north' and row < self.size - 1:  # Node below (south)
            self.maze.add_edge(current_node, current_node + self.size)
        elif front and front_direction == 'east' and col > 0:  # Node to the left (west)
            self.maze.add_edge(current_node, current_node - 1)

        if right and right_direction == 'south' and row > 0:  # Node above (north)
            self.maze.add_edge(current_node, current_node - self.size)
        elif right and right_direction == 'west' and col < self.size - 1:  # Node to the right (east)
            self.maze.add_edge(current_node, current_node + 1)
        elif right and right_direction == 'north' and row < self.size - 1:  # Node below (south)
            self.maze.add_edge(current_node, current_node + self.size)
        elif right and right_direction == 'east' and col > 0:  # Node to the left (west)
            self.maze.add_edge(current_node, current_node - 1)

        if left and left_direction == 'south' and row > 0:  # Node above (north)
            self.maze.add_edge(current_node, current_node - self.size)
        elif left and left_direction == 'west' and col < self.size - 1:  # Node to the right (east)
            self.maze.add_edge(current_node, current_node + 1)
        elif left and left_direction == 'north' and row < self.size - 1:  # Node below (south)
            self.maze.add_edge(current_node, current_node + self.size)
        elif left and left_direction == 'east' and col > 0:  # Node to the left (west)
            self.maze.add_edge(current_node, current_node - 1)

        if back and back_direction == 'south' and row > 0:  # Node above (north)
            self.maze.add_edge(current_node, current_node - self.size)
        elif back and back_direction == 'west' and col < self.size - 1:  # Node to the right (east)
            self.maze.add_edge(current_node, current_node + 1)
        elif back and back_direction == 'north' and row < self.size - 1:  # Node below (south)
            self.maze.add_edge(current_node, current_node + self.size)
        elif back and back_direction == 'east' and col > 0:  # Node to the left (west)
            self.maze.add_edge(current_node, current_node - 1)

    def display_maze(self):
        """
        Displays the maze graph in a square grid layout with visited nodes highlighted.
        
        Visited nodes are colored light green, while unvisited nodes are light blue.
        """
        # Create a grid layout for the nodes
        pos = {
            node: (self.size - 1 - (node % self.size),
                   self.size - 1 - (node // self.size))
            for node in self.maze.nodes
        }
        pos = {node: (x, self.size - 1 - y) for node, (x, y) in pos.items()}

        # Generate color mapping for nodes based on visitation status
        color_map = [
            'lightgreen' if node in self.visited_nodes else 'lightblue'
            for node in self.maze.nodes
        ]

        # Display the maze using Matplotlib
        plt.figure(figsize=(16, 9))
        nx.draw(self.maze,
                pos,
                with_labels=True,
                node_color=color_map,
                edge_color='gray',
                node_size=140,
                font_size=7)
        plt.show()

    def save_maze(self, filepath, format='png'):
        """
        Saves the maze graph as an image file (PNG or SVG).

        Parameters:
        -----------
        filepath : str
            The file path where the maze image will be saved.
        format : str, optional
            The format of the saved file ('png' or 'svg', default is 'png').
        """
        # Create a grid layout for the nodes
        pos = {
            node: (self.size - 1 - (node % self.size),
                   self.size - 1 - (node // self.size))
            for node in self.maze.nodes
        }
        pos = {node: (x, self.size - 1 - y) for node, (x, y) in pos.items()}

        # Generate color mapping for nodes based on visitation status
        color_map = [
            'lightgreen' if node in self.visited_nodes else 'lightblue'
            for node in self.maze.nodes
        ]

        # Draw the maze graph
        plt.figure(figsize=(16, 9))
        nx.draw(self.maze,
                pos,
                with_labels=True,
                node_color=color_map,
                edge_color='gray',
                node_size=140,
                font_size=7)

        # Save the figure to the specified file path
        plt.savefig(filepath + '.' + format, format=format)
        plt.close()

    def load_maze(self, df):
        """
        Loads maze structure from a pandas DataFrame and adds edges to the maze graph.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing maze data with columns: ['current_cell', 'facing', 'right', 'front', 'left'].
        """
        for _, row in df.iterrows():
            current_cell = int(row['current_cell'])
            self.add_edges(
                current_node=current_cell,
                facing_direction=row['facing'],
                front=row['front'],
                right=row['right'],
                left=row['left'],
            )

    def is_straight_line(self, nodes: list[int]):
        """
        Return True if all nodes make a straight line else returns False.
        """
        if len(nodes) <= 2:
            return True

        if (nodes[0] + 1 == nodes[1]) or (nodes[0] - 1 == nodes[1]):
            diff = 1
        else:
            diff = 16

        for i in range(2, len(nodes)):
            if abs(nodes[i - 1] - nodes[i]) != diff:
                return False

        return True

    def get_all_lines(self, nodes: list):
        """
        Splits the input list into sublists of continuous lines (straight paths).

        Parameters:
        -----------
        nodes : list
            List of node numbers.

        Returns:
        --------
        list
            A list of sublists, where each sublist represents a continuous straight path.
        """
        if len(nodes) < 2:
            return [nodes]  # If less than two nodes, return as a single group

        lines = []
        stack = []
        for i in range(0, len(nodes)):
            stack.append(nodes[i])
            if not self.is_straight_line(stack):
                stack.pop()
                lines.append(stack)
                stack = [nodes[i - 1], nodes[i]]
            i += 1

        if len(stack) >= 2:
            lines.append(stack)
        return lines

    @classmethod
    def get_direction_to_turn(cls, from_n: int, to_n: int):
        """Returns a string("north", "east", "south", "west"), based on the direction one needs to move in to get from from_n to to_n."""

        diff = from_n - to_n

        if diff == 1:
            return "east"
        elif diff == -1:
            return "west"
        elif diff == 16:
            return "south"
        elif diff == -16:
            return "north"
        else:
            return -1

    def generate_shortest_path_commands(
        self,
        from_node,
        to_node,
        initial_facing="north",
        cell_width_hight=35,
    ):
        """
        Generates movement commands to traverse the shortest path from 'from_node' to 'to_node',
        taking into account the initial facing direction.
    
        Parameters:
        -----------
        from_node : int
            The starting node.
        to_node : int
            The destination node.
        initial_facing : str
            The initial facing direction ("north", "east", "south", "west").
    
        Returns:
        --------
        commands : list of str
            A list of commands to follow the shortest path.
        """
        paths = self.get_all_lines(
            nx.shortest_path(self.maze, source=from_node, target=to_node))
        commands = []
        directions = {"north": 270, "east": 0, "south": 90, "west": 180}
        current_facing = initial_facing

        for path in paths:
            face_to = MicroMouseMaze.get_direction_to_turn(path[0], path[1])
            if face_to != current_facing:
                commands.append(["r", directions[face_to]])
                current_facing = face_to
            commands.append([
                "l2",
                self.__distance_mouse_will_see_after_travel(
                    path, cell_width_hight=cell_width_hight)
            ])

        return commands

    def get_cell_to_explore(self, stack):
        """
        Identifies the next cell to explore based on unvisited neighbors.

        This method iterates through the stack in reverse order (excluding the last cell) to find neighbors of each cell.
        It checks whether a path exists between the current cell and its neighbors using NetworkX and evaluates whether
        the neighbor has already been visited. If unvisited, the neighbor is added to the list of exploration options.

        Parameters:
        -----------
        stack : list
            Stack of cells representing the path explored so far.

        Returns:
        --------
        int
            A randomly selected neighboring cell that is unvisited and can be explored next.
        """
        options = []
        for cell in stack[
                -2::
                -1]:  # Iterate through stack in reverse order, skipping the last element
            # Calculate neighbors: left, right, top, bottom
            neighbours = [
                cell + 1, cell - 1, cell + self.size, cell - self.size
            ]
            for nei in neighbours:
                try:
                    # Check if there is a path between cell and neighbor
                    nx.shortest_path(self.maze, source=cell, target=nei)
                    if not self.is_visited(nei):
                        options.append(nei)
                except:
                    pass
            if len(options) != 0:
                break

        l.info(f"STACK: {stack}")
        l.info(f"CELLS CAN BE EXPLORE: {options}")

        return random.choice(options)

    def __distance_mouse_will_see_after_travel(self, path, cell_width_hight):
        """
        Calculates the distance the mouse can see after traveling along a given path.

        This function computes the number of cells the mouse can see in a straight line after reaching the last cell 
        in the path. It checks for obstacles or turns and stops counting if no straight path is found.

        Parameters:
        -----------
        path : list
            List of cell numbers representing the traveled path.
        cell_width_hight : float
            Width or height of a single cell in the grid (assumes square cells).

        Returns:
        --------
        float
            Total visible distance based on the number of cells in front and their size.
        """
        diff = path[0] - path[1]
        number_of_cell_in_front = 0
        current_cell = path[-1]
        while True:
            try:
                # Check if there is a straight path to the next cell
                path = nx.shortest_path(self.maze,
                                        source=current_cell,
                                        target=current_cell - diff)
                current_cell -= diff
                if len(path) > 2:
                    # No straight path
                    break
                number_of_cell_in_front += 1
            except:
                # No valid path
                break
        return (cell_width_hight / 2) + (number_of_cell_in_front * 35)

    @classmethod
    def check_intersection_with_curve(
        cls,
        position,  # [x, y]
        angle,  # radians
        threshold_distance=1,
    ):
        #todo deal with edge cases
        min_for_line, max_for_line = position[
            0] - threshold_distance, position[0] + threshold_distance
        __line_eq = cls.line_eq.subs({
            h: position[0],
            k: position[1],
            theta: angle
        })
        if angle % math.pi / 2 == 0:
            angle = angle * 1.0001
        if position[0] == 0:
            position[0] = 0.000001
        # print(position, angle)
        try:
            sol = sp.nsolve(cls.path_eq - __line_eq, x,
                            (min_for_line + max_for_line) / 2)
            if not (sol <= max_for_line and sol >= min_for_line):
                sol = position[0]
        except Exception as e:
            sol = position[0]

        dist = math.hypot(
            position[0] - sol,
            position[1] - float(__line_eq.subs(
                x,
                sol,
            ), ),
        )

        if position[1] - float(cls.path_eq.subs(x, position[0])) > 0:
            return (-1) * dist

        return dist


if __name__ == "__main__":
    # Example usage
    mouse_maze = MicroMouseMaze(size=16)
    # Add edges based on open paths (e.g., front, right, left, back)
    """
    mouse_maze.add_edges(
        151,
        front=False,
        right=False,
        left=True,
        back=False,
        facing_direction="east",
    )
    mouse_maze.add_edges(
        169,
        front=True,
        right=False,
        left=False,
        back=False,
        facing_direction="south",
    )
    mouse_maze.add_edges(
        147,
        front=True,
        right=False,
        left=False,
        back=False,
        facing_direction="east",
    )
"""

    df = pd.read_csv("bin/mazes/maze_data 2024-12-20, 20 07 25.csv")
    mouse_maze.load_maze(df)
    # Display the maze
    mouse_maze.display_maze()

    # Save the maze to a file
    # mouse_maze.save_maze("maze_output.png", format="png")
