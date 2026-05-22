import nashpy as nash
import numpy as np

# Payoff matrices
A = np.array([[3, 1, 0],
              [2, 2, 1],
              [0, 0, 4]])

B = np.array([[3, 2, 0],
              [1, 2, 0],
              [0, 1, 3]])

game = nash.Game(A, B)

print("  Nash Equilibrium Solver — Vertex Enumeration")

equilibria = list(game.vertex_enumeration())

if not equilibria:
    print("\nNo equilibria found.")
else:
    for i, (p1, p2) in enumerate(equilibria, 1):
        print(f"\n  Equilibrium {i}:")
        print(f"    Player 1 strategy: {np.round(p1, 4)}")
        print(f"    Player 2 strategy: {np.round(p2, 4)}")

        # Compute expected payoffs
        payoff_1 = p1 @ A @ p2
        payoff_2 = p1 @ B @ p2
        print(f"    Expected payoff P1: {payoff_1:.4f}")
        print(f"    Expected payoff P2: {payoff_2:.4f}")

print(f"  Total vertices found: {len(equilibria)}")
