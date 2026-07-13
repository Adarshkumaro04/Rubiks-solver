import twophase.solver as sv
import time

# ANSI color codes for terminal display
COLORS = {
    'U': '\033[97m U \033[0m',  # white
    'R': '\033[91m R \033[0m',  # red
    'F': '\033[92m F \033[0m',  # green
    'D': '\033[93m D \033[0m',  # yellow
    'L': '\033[38;5;208m L \033[0m',  # orange
    'B': '\033[94m B \033[0m',  # blue
}

def print_cube(cubestring):
    """Prints a 2D unfolded net of the cube given its 54-char facelet string."""
    faces = {
        'U': cubestring[0:9],
        'R': cubestring[9:18],
        'F': cubestring[18:27],
        'D': cubestring[27:36],
        'L': cubestring[36:45],
        'B': cubestring[45:54],
    }

    def row(face, r):
        return ''.join(COLORS[c] for c in faces[face][r*3:(r+1)*3])

    print()
    for r in range(3):
        print('            ' + row('U', r))
    for r in range(3):
        print(row('L', r) + row('F', r) + row('R', r) + row('B', r))
    for r in range(3):
        print('            ' + row('D', r))
    print()

# Human-readable move translation
FACE_NAMES = {'U': 'Up', 'R': 'Right', 'F': 'Front', 'D': 'Down', 'L': 'Left', 'B': 'Back'}
TURN_NAMES = {'1': '90° clockwise', '2': '180°', '3': '90° counter-clockwise'}

def explain_moves(solution_str):
    moves = solution_str.split('(')[0].strip().split()
    print("Step-by-step:")
    for i, move in enumerate(moves, 1):
        face, turn = move[0], move[1]
        print(f"  {i}. {move} → Turn {FACE_NAMES[face]} face {TURN_NAMES[turn]}")

def main():
    print("=== Rubik's Cube Solver (Two-Phase Algorithm) ===")
    cubestring = input("Enter cube definition string (or press Enter for demo cube): ").strip()

    if not cubestring:
        cubestring = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'
        print(f"Using demo cube: {cubestring}")

    print("\nScrambled cube:")
    print_cube(cubestring)

    print("Solving...")
    start = time.time()
    solution = sv.solve(cubestring, 19, 2)
    elapsed = time.time() - start

    print(f"\nSolution: {solution}")
    print(f"Solved in {elapsed:.3f} seconds\n")
    explain_moves(solution)

if __name__ == "__main__":
    main()