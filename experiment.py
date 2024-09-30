import matplotlib.pyplot as plt
from logic import PyraminxPuzzle
from solver import solve_puzzle
import random
import time


def generate_random_puzzle(k):
    puzzle = PyraminxPuzzle()
    faces = ["F", "L", "R", "B"]
    directions = ["clockwise", "counterclockwise"]
    move_sequence = [(random.choice(faces), random.choice(directions)) for _ in range(k)]
    
    for move in move_sequence:
        puzzle.apply_rotation(*move)
    
    print("Generated Puzzle (after scrambling):")
    puzzle.print_puzzle()  # Display the generated puzzle for debugging
    return puzzle

def run_experiment():
    ks = range(3, 5)  # Number of moves to scramble the puzzle
    average_nodes = []
    solved_instances = []

    for k in ks:
        print(f"Running experiments for k={k}")
        nodes_list = []
        solved = 0
        for i in range(5):
            print(f"  Instance {i+1}/5")
            puzzle = generate_random_puzzle(k)
            start_time = time.time()
            
            try:
                # Attempt to solve the puzzle and capture solution and nodes expanded
                solution, nodes_expanded = solve_puzzle(puzzle)
            except Exception as e:
                print(f"Error solving puzzle instance {i+1}: {e}")
                nodes_expanded = 0
            
            end_time = time.time()
            if solution:
                nodes_list.append(nodes_expanded)
                solved += 1
                print(f"    Solved in {len(solution)} moves with {nodes_expanded} nodes expanded in {end_time - start_time:.2f} seconds.")
            else:
                nodes_list.append(0)
                print(f"    No solution found.")
        
        # Compute average, ignoring unsolved instances
        valid_nodes = [n for n in nodes_list if n > 0]
        avg = sum(valid_nodes) / len(valid_nodes) if valid_nodes else 0
        average_nodes.append(avg)
        solved_instances.append(solved)

    # Plotting Average Nodes Expanded
    plt.figure(figsize=(10, 6))
    plt.plot(ks, average_nodes, marker='o', label='Average Nodes Expanded')
    plt.xlabel('Number of Random Moves (k)')
    plt.ylabel('Average Number of Nodes Expanded')
    plt.title('A* Search Performance on 4x4 Pyraminx')
    plt.grid(True)
    plt.legend()
    plt.savefig('a_star_performance.png')
    plt.show()

    # Plotting Solved Instances
    plt.figure(figsize=(10, 6))
    plt.plot(ks, solved_instances, marker='x', color='red', label='Solved Instances out of 5')
    plt.xlabel('Number of Random Moves (k)')
    plt.ylabel('Number of Solved Instances')
    plt.title('Solver Success Rate on 4x4 Pyraminx')
    plt.grid(True)
    plt.legend()
    plt.savefig('solver_success_rate.png')
    plt.show()

if __name__ == "__main__":
    run_experiment()

