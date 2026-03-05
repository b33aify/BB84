from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import numpy as np

app = Flask(__name__)
CORS(app)

ket_0 = np.array([[1], [0]])
ket_1 = np.array([[0], [1]])

ket_plus = (1 / np.sqrt(2)) * (ket_0 + ket_1)
ket_minus = (1 / np.sqrt(2)) * (ket_0 - ket_1)


def prepare_qubit(bit, basis):
    if basis == '+':
        return ket_0 if bit == 0 else ket_1
    else:
        return ket_plus if bit == 0 else ket_minus


def measure_qubit_mathematically(state_vector, measurement_basis):
    if measurement_basis == '+':
        basis_0 = ket_0
        basis_1 = ket_1
    else:
        basis_0 = ket_plus
        basis_1 = ket_minus

    projection_0 = np.vdot(basis_0, state_vector)
    prob_0 = abs(projection_0) ** 2

    prob_1 = 1 - prob_0

    measured_bit = np.random.choice([0, 1], p=[prob_0, prob_1])

    collapsed_state = basis_0 if measured_bit == 0 else basis_1

    return measured_bit, collapsed_state


@app.route('/simulate', methods=['POST'])
def simulate_bb84():
    data = request.json
    num_bits = int(data.get('num_bits', 12))
    eve_present = data.get('eve_present', False)

    alice_bits = [random.choice([0, 1]) for _ in range(num_bits)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]

    quantum_states = [prepare_qubit(b, base) for b, base in zip(alice_bits, alice_bases)]

    polarizations = []
    for b, basis in zip(alice_bits, alice_bases):
        if basis == '+':
            polarizations.append('↑' if b == 0 else '→')
        else:
            polarizations.append('↗' if b == 0 else '↘')

    eve_bases = [None] * num_bits

    if eve_present:
        eve_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
        for i in range(num_bits):
            measured_bit, collapsed_vector = measure_qubit_mathematically(
                quantum_states[i],
                eve_bases[i]
            )
            quantum_states[i] = collapsed_vector

    bob_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
    bob_results = []

    for i in range(num_bits):
        measured_bit, _ = measure_qubit_mathematically(
            quantum_states[i],
            bob_bases[i]
        )
        bob_results.append(int(measured_bit))

    sifted_alice = []
    sifted_bob = []
    match_indices = []

    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            match_indices.append(True)
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_results[i])
        else:
            match_indices.append(False)

    errors = 0
    for a, b in zip(sifted_alice, sifted_bob):
        if a != b:
            errors += 1

    total_sifted = len(sifted_alice)
    qber = (errors / total_sifted * 100) if total_sifted > 0 else 0
    key_secure = (errors == 0)

    return jsonify({
        'alice_bits': alice_bits,
        'alice_bases': alice_bases,
        'polarizations': polarizations,
        'bob_bases': bob_bases,
        'bob_results': bob_results,
        'match_indices': match_indices,
        'sifted_key': sifted_bob,
        'qber': qber,
        'key_secure': key_secure
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)