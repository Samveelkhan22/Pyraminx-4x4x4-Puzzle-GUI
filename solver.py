from logic import PyraminxPuzzle

def solve_puzzle(initial_puzzle):
    """
    Solves the Pyraminx puzzle using A* search.
    """
    print("Puzzle before solving:")
    initial_puzzle.print_puzzle()  # Display the puzzle before solving
    
    try:
        solution, nodes = initial_puzzle.solve_a_star()
    except Exception as e:
        print(f"Error while solving: {e}")
        return None, 0
    
    if solution:
        print("\nSolution:", solution)
        print(f"Nodes expanded: {nodes}")
    else:
        print("No solution found.")
    
    print("\nPuzzle after solving:")
    initial_puzzle.print_puzzle()  # Display the puzzle after solving

    # Return the solution and number of nodes expanded
    return solution, nodes

if __name__ == "__main__":
    puzzle = PyraminxPuzzle()
    
    # Scramble the puzzle with some rotations (example scramble)
    puzzle.apply_rotation("F", "clockwise")
    puzzle.apply_rotation("L", "counterclockwise")
    
    # Solve the puzzle
    solve_puzzle(puzzle)
