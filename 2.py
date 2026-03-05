import numpy as np
import random

# --- 1. DEFINE THE PHYSICS ---

# The States (Vectors)
# |0>
ZERO = np.array([[1],
                 [0]])
# |1>
ONE = np.array([[0],
                [1]])

# The Gates (Matrices)
# Identity (Does nothing)
ID = np.array([[1, 0],
               [0, 1]])

# Hadamard (Creates Superposition)
# This is the magic matrix that turns |0> into 50% 0 and 50% 1
H = (1 / np.sqrt(2)) * np.array([[1, 1],
                                 [1, -1]])


def get_qubit_state(bit, basis):
    """
    Creates the mathematical vector for a qubit.
    Basis 0 (Rectilinear): Returns |0> or |1>
    Basis 1 (Diagonal):    Returns H|0> or H|1> (+ or -)
    """
    # Start with the basic state |0> or |1>
    state = ZERO if bit == 0 else ONE

    # If using Diagonal basis (1), apply Hadamard matrix
    if basis == 1:
        # Matrix Multiplication: H * state
        state = np.dot(H, state)

    return state


def measure_qubit_math(qubit_vector, bob_basis):
    """
    Simulates measurement using Linear Algebra probabilities.
    """
    # 1. Prepare Bob's measurement "filter"
    # If Bob measures in Diagonal (1), we must apply H to the qubit
    # to bring it back to the standard basis for measuring.
    measure_operator = H if bob_basis == 1 else ID

    # 2. Transform the state vector relative to Bob
    final_state = np.dot(measure_operator, qubit_vector)

    # 3. Calculate Probabilities (The Born Rule)
    # Probability of 0 is the square of the top number (Amplitude alpha)
    # Probability of 1 is the square of the bottom number (Amplitude beta)
    prob_0 = final_state[0, 0] ** 2
    # (We round to avoid tiny floating point errors like 0.9999999)
    prob_0 = round(prob_0, 5)

    # 4. Collapse the wavefunction
    # We pick 0 or 1 based on the calculated probability
    result = np.random.choice([0, 1], p=[prob_0, 1 - prob_0])
    return result


# --- 2. THE SIMULATION ---

# Example: Alice sends Bit 0 in Basis 1 (Diagonal) -> State |+>
alice_bit = 0
alice_basis = 1
# Bob uses Basis 0 (Rectilinear) -> Mismatch!
bob_basis = 0

print(f"Alice sends bit {alice_bit} in basis {alice_basis}")
print(f"Bob measures in basis {bob_basis}")

# Get the vector
q_vector = get_qubit_state(alice_bit, alice_basis)
print(f"\nQubit Vector (Math):\n{q_vector}")

# Measure
measured_bit = measure_qubit_math(q_vector, bob_basis)
print(f"\nBob Measured: {measured_bit}")