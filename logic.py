# logic.py

import copy
import heapq
from itertools import count  # Import count for tie-breaking

class PyraminxPuzzle:
    def __init__(self):
        # Initialize the puzzle in the solved state
        # Each face is represented as a 4x4 grid
        self.faces = {
            "F": [['red'] * 4 for _ in range(4)],
            "L": [['green'] * 4 for _ in range(4)],
            "R": [['blue'] * 4 for _ in range(4)],
            "B": [['yellow'] * 4 for _ in range(4)]
        }

    def apply_rotation(self, face, direction):
        """
        Rotates the specified face in the given direction.
        Also updates the adjacent faces accordingly.

        :param face: One of 'F', 'L', 'R', 'B'
        :param direction: 'clockwise' or 'counterclockwise'
        """
        if face not in self.faces or direction not in ["clockwise", "counterclockwise"]:
            raise ValueError("Invalid face or direction")

        # Rotate the face's own grid
        self.faces[face] = self.rotate_face(self.faces[face], direction)

        # Update adjacent faces
        self.update_adjacent_faces(face, direction)

    def rotate_face(self, grid, direction):
        """
        Rotates a 4x4 grid clockwise or counterclockwise.

        :param grid: 4x4 list representing the face
        :param direction: 'clockwise' or 'counterclockwise'
        :return: Rotated 4x4 grid
        """
        if direction == "clockwise":
            return [list(row) for row in zip(*grid[::-1])]
        else:
            return [list(row) for row in zip(*grid)][::-1]

    def update_adjacent_faces(self, face, direction):
        """
        Updates the adjacent faces based on the rotation of the specified face.

        :param face: The face being rotated
        :param direction: The direction of rotation
        """
        # Define the mapping of affected rows for each face rotation
        # Each face rotation affects three adjacent faces
        # The indices specify which rows are affected

        # Define the order of adjacent faces for each face
        adjacent_faces = {
            "F": ["L", "R", "B"],
            "L": ["B", "R", "F"],
            "R": ["F", "B", "L"],
            "B": ["R", "L", "F"]
        }

        # Define which row index is affected on each adjacent face
        # Assuming that the top row (index 0) is the one adjacent to the current face
        # Adjust indices as per actual Pyraminx mechanics
        affected_rows = {
            "F": [0, 0, 0],  # Front rotation affects top rows of L, R, B
            "L": [0, 0, 0],  # Left rotation affects top rows of B, R, F
            "R": [0, 0, 0],  # Right rotation affects top rows of F, B, L
            "B": [0, 0, 0]   # Back rotation affects top rows of R, L, F
        }

        # Get the list of adjacent faces in the rotation order
        adj = adjacent_faces[face]
        rows = affected_rows[face]

        # Extract the affected lines
        lines = []
        for adj_face, row_idx in zip(adj, rows):
            lines.append(self.get_row(adj_face, row_idx))

        # Rotate the lines based on direction
        if direction == "clockwise":
            rotated = [lines[-1]] + lines[:-1]
        else:
            rotated = lines[1:] + [lines[0]]

        # Assign the rotated lines back to the adjacent faces
        for adj_face, row_idx, new_line in zip(adj, rows, rotated):
            self.set_row(adj_face, row_idx, new_line)

    def get_row(self, face, row):
        """
        Retrieves a specific row from a face.

        :param face: Face name ('F', 'L', 'R', 'B')
        :param row: Row index (0 to 3)
        :return: List of colors in the row
        """
        return self.faces[face][row][:]

    def set_row(self, face, row, new_row):
        """
        Sets a specific row on a face.

        :param face: Face name ('F', 'L', 'R', 'B')
        :param row: Row index (0 to 3)
        :param new_row: List of colors to set in the row
        """
        self.faces[face][row] = new_row

    def get_face(self, face):
        """
        Retrieves the current state of a specific face.

        :param face: Face name ('F', 'L', 'R', 'B')
        :return: 4x4 grid of colors
        """
        return self.faces.get(face, [['black'] * 4 for _ in range(4)])

    def is_solved(self):
        """
        Checks if the puzzle is in a solved state.

        :return: True if solved, False otherwise
        """
        for face, grid in self.faces.items():
            color = grid[0][0]
            for row in grid:
                for cell in row:
                    if cell != color:
                        return False
        return True

    def copy(self):
        """
        Creates a deep copy of the puzzle.

        :return: A new PyraminxPuzzle instance
        """
        return copy.deepcopy(self)

    def __eq__(self, other):
        return self.faces == other.faces

    def __hash__(self):
        # Convert the state to a tuple of tuples for hashing
        state = tuple(tuple(tuple(row) for row in self.faces[face]) for face in sorted(self.faces))
        return hash(state)

    def get_possible_moves(self):
        """
        Generates all possible moves (face rotations).

        :return: List of (face, direction) tuples
        """
        faces = ["F", "L", "R", "B"]
        directions = ["clockwise", "counterclockwise"]
        moves = [(face, direction) for face in faces for direction in directions]
        return moves

    def heuristic(self):
        """
        Admissible heuristic: Counts the number of misplaced small triangles.

        :return: Heuristic value
        """
        misplaced = 0
        for face, grid in self.faces.items():
            expected_color = grid[0][0]
            for row in grid:
                for cell in row:
                    if cell != expected_color:
                        misplaced += 1
        return misplaced

    def solve_a_star(self):
        """
        Solves the puzzle using the A* search algorithm.

        :return: (solution_path, nodes_expanded)
        """
        start_state = self.copy()
        goal_state = PyraminxPuzzle()  # Solved state

        open_set = []
        counter = count()  # Initialize a counter for tie-breaking
        heapq.heappush(open_set, (start_state.heuristic(), next(counter), start_state))
        came_from = {}
        g_score = {start_state: 0}
        nodes_expanded = 0

        closed_set = set()

        while open_set:
            current_f, _, current = heapq.heappop(open_set)

            if current.is_solved():
                # Reconstruct path
                path = []
                while current in came_from:
                    current, move = came_from[current]
                    path.append(move)
                return path[::-1], nodes_expanded

            if current in closed_set:
                continue  # Skip already processed states

            closed_set.add(current)
            nodes_expanded += 1

            for move in current.get_possible_moves():
                face, direction = move
                neighbor = current.copy()
                neighbor.apply_rotation(face, direction)
                tentative_g = g_score[current] + 1

                if neighbor in closed_set:
                    continue  # Skip already processed neighbors

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = (current, move)
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + neighbor.heuristic()
                    heapq.heappush(open_set, (f_score, next(counter), neighbor))

        return None, nodes_expanded

    def print_puzzle(self):
        """
        Prints the current state of the puzzle in a more readable format.
        """
        print("Front Face (F):")
        for row in self.faces['F']:
            print(row)
        
        print("\nLeft Face (L):")
        for row in self.faces['L']:
            print(row)
        
        print("\nRight Face (R):")
        for row in self.faces['R']:
            print(row)
        
        print("\nBack Face (B):")
        for row in self.faces['B']:
            print(row)