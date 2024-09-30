import tkinter as tk
from tkinter import messagebox
import random
from PIL import ImageGrab
import cv2
import numpy as np
from logic import PyraminxPuzzle
from solver import solve_puzzle

class PyraminxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pyraminx 4x4x4 Puzzle")

        self.puzzle = PyraminxPuzzle()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.canvas = tk.Canvas(self.frame, width=800, height=400, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # Create a frame for controls and logging
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.log_text = tk.Text(self.control_frame, width=50, height=10, wrap=tk.WORD)
        self.log_text.pack(pady=10)
        self.log_text.insert(tk.END, "Log:\n")

        self.draw_pyraminx_faces()
        self.create_controls()

    def draw_pyraminx_faces(self):
        self.canvas.delete("all")  # Clear previous drawings
        positions = {
            "L": (100, 100),
            "F": (300, 100),
            "R": (500, 100),
            "B": (400, 400)
        }

        for face, (offset_x, offset_y) in positions.items():
            if face == "B":
                self.draw_triangle_grid(self.canvas, face, offset_x, offset_y, invert_y=True, mirror_x=True)
            else:
                self.draw_triangle_grid(self.canvas, face, offset_x, offset_y)

    def draw_triangle_grid(self, canvas, face, offset_x, offset_y, invert_y=False, mirror_x=False):
        triangle_size = 40
        height = triangle_size * (3 ** 0.5) / 2
        num_rows = 4

        grid = self.puzzle.get_face(face)

        for r in range(num_rows):
            for c in range(r + 1):
                x1 = offset_x + (num_rows - r - 1) * (triangle_size / 2) + c * triangle_size
                y1 = offset_y + r * height
                x2 = x1 + triangle_size / 2
                y2 = y1 + height
                x3 = x1 - triangle_size / 2
                y3 = y1 + height

                if invert_y:
                    y1 = -y1 + 2 * offset_y
                    y2 = -y2 + 2 * offset_y
                    y3 = -y3 + 2 * offset_y
                if mirror_x:
                    x1 = -x1 + 2 * offset_x
                    x2 = -x2 + 2 * offset_x
                    x3 = -x3 + 2 * offset_x

                try:
                    color = grid[r][c]
                except IndexError:
                    color = 'red'  # Default color if out of bounds

                canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline='black', fill=color)

    def create_controls(self):
        control_panel = tk.Frame(self.control_frame)
        control_panel.pack()

        tk.Label(control_panel, text="Number of Random Moves (k):").grid(row=0, column=0, padx=5, pady=5)
        self.num_moves_entry = tk.Entry(control_panel, width=5)
        self.num_moves_entry.insert(0, "10")
        self.num_moves_entry.grid(row=0, column=1, padx=5, pady=5)

        self.randomize_button = tk.Button(control_panel, text="Shuffle", command=self.randomize_puzzle)
        self.randomize_button.grid(row=0, column=2, padx=5, pady=5)

        self.solve_button = tk.Button(control_panel, text="Solve", command=self.solve_puzzle)
        self.solve_button.grid(row=0, column=3, padx=5, pady=5)

    def generate_random_moves(self, num_moves):
        faces = ["F", "L", "R", "B"]
        directions = ["clockwise", "counterclockwise"]
        move_sequence = [(random.choice(faces), random.choice(directions)) for _ in range(num_moves)]
        return move_sequence

    def log_message(self, message):
        """Log a message to the Text widget."""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

    def randomize_puzzle(self):
        try:
            moves = int(self.num_moves_entry.get())
            self.log_message(f"Randomizing Pyraminx with {moves} moves.")

            move_sequence = self.generate_random_moves(moves)

            for face, direction in move_sequence:
                self.log_message(f"Rotated {face} face {direction}")
                self.record_move(face, direction)
                self.puzzle.apply_rotation(face, direction)
                self.draw_pyraminx_faces()
                self.root.update_idletasks()
                self.root.after(500)  # Delay for animation effect

            self.log_message("Puzzle randomized!\n")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of moves")

    def record_move(self, face, direction):
        # Set up video recording
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('move_record.avi', fourcc, 20.0, (800, 600))  # Adjust resolution as needed

        # Capture the initial frame
        self.draw_pyraminx_faces()  # Ensure the GUI is updated before capturing
        img = self.get_screenshot()
        out.write(img)

        # Perform the rotation
        self.puzzle.apply_rotation(face, direction)

        # Capture the frame after the move
        self.draw_pyraminx_faces()  # Update the GUI again
        img = self.get_screenshot()
        out.write(img)

        # Finalize the video
        out.release()

    def get_screenshot(self):
        # Grab the current state of the tkinter canvas
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Capture the screenshot using ImageGrab
        img = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Convert the PIL image to a NumPy array (compatible with OpenCV)
        img_np = np.array(img)

        # Convert RGB to BGR (OpenCV expects images in BGR format)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        return img_np

    def solve_puzzle(self):
        self.log_message("Starting to solve the puzzle...")
        self.root.update_idletasks()

        solution_steps, nodes_expanded = solve_puzzle(self.puzzle.copy())

        if solution_steps is None:
            self.log_message("No solution found.")
            return

        for move in solution_steps:
            face, direction = move
            self.log_message(f"Rotated {face} face {direction}")
            self.puzzle.apply_rotation(face, direction)
            self.draw_pyraminx_faces()
            self.root.update_idletasks()
            self.root.after(500)  # Delay for animation effect

        self.log_message(f"Puzzle solved in {len(solution_steps)} moves with {nodes_expanded} nodes expanded!\n")

# Ensure to handle video cleanup and error management as necessary in production
