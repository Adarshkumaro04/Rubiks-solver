import twophase.solver as sv

def main():
    print("=== Rubik's Cube Solver (Two-Phase Algorithm) ===")
    cubestring = input("Enter cube definition string (or press Enter for demo cube): ").strip()
    
    if not cubestring:
        cubestring = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'
        print(f"Using demo cube: {cubestring}")
    
    print("\nSolving...")
    solution = sv.solve(cubestring, 19, 2)
    print(f"\nSolution: {solution}")

if __name__ == "__main__":
    main()