# Rubik's Cube Solver

A Python project that solves a scrambled Rubik's Cube using the two-phase algorithm. 
Give it a scrambled cube state, it gives you back the moves to solve it — usually 
under 20 moves, in a couple of seconds.

## Why I picked this project

I wanted something that involved real search/optimization concepts, not just another 
CRUD app. Solving a Rubik's Cube sounds simple but the state space is huge — there are 
about 43 quintillion possible cube positions — so brute-forcing it is out of the 
question. That's what got me interested in how the two-phase algorithm actually cuts 
this down to something solvable in seconds.

## How it works (short version)

Instead of searching for a solution across the entire cube state at once, the algorithm 
splits the problem into two smaller steps:

1. **Phase 1** — get the cube into a specific "easier" subgroup of states, where 
   corners/edges are oriented correctly even if not in their final spot yet.
2. **Phase 2** — from that subgroup, solve the rest using a smaller set of moves.

Both phases use precomputed tables that tell the algorithm roughly how far a state is 
from solved, so it's not searching blindly. These tables take about 30 min to build the 
first time you run it, but after that solving is basically instant.

## What's actually mine here

I'll be upfront: the core solving algorithm (the two-phase logic + pruning tables) is 
from Herbert Kociemba's `RubikTwoPhase` library — I installed it via pip rather than 
writing the algorithm from scratch. What I did myself:

- Read through how the algorithm works and got comfortable enough to explain it
- Wrote `main.py` as a simple CLI so you don't have to mess with the raw library in a 
  Python shell
- Tested it end-to-end and wrote this README

I think that's a reasonable way to build on a hard, already-solved problem instead of 
badly reinventing it — same idea as using OpenCV instead of writing your own image 
processing from scratch.

## Running it

```bash
pip install -r requirements.txt
python -c "import twophase.solver"   # first time only, builds tables, takes a while
python main.py
```

Then either paste in a 54-character cube string when it asks, or just hit Enter to run 
a demo scramble.

## Example

Input:
DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL

Output:
L3 U1 B1 R2 F3 L1 F3 U2 L1 U3 B3 U2 B1 L2 F1 U2 R2 L2 B2 (19f)

## Things I'd add if I had more time

- A visual animation of the moves instead of just text
- Scanning a real cube's colors with a webcam instead of typing the string manually
- Comparing this against a truly optimal solver to see the speed vs. move-count tradeoff

## Credit

Solving algorithm by [Herbert Kociemba](https://github.com/hkociemba/RubiksCube-TwophaseSolver). 
I built the CLI wrapper around his `RubikTwoPhase` package.