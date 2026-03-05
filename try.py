import random

def generate_random_bits(length):
    return [random.choice([0, 1]) for _ in range(length)]

def measure_qubits(alice_bits, alice_bases, bob_bases):
    bob_results = []

    for i in range(len(alice_bits)):
        a_bit = alice_bits[i]
        a_basis = alice_bases[i]
        b_basis = bob_bases[i]

        if a_basis == b_basis:
            bob_results.append(a_bit)
        else:
            bob_results.append(random.choice([0, 1]))

    return bob_results

def sift_keys(alice_bases, bob_bases, bob_results):
    sifted_key = []
    for i in range(len(alice_bases)):
        if alice_bases[i] == bob_bases[i]:
            sifted_key.append(bob_results[i])

    return sifted_key

def intercept_qubits(alice_bits, alice_bases):
    eve_bases = generate_random_bits(len(alice_bits))
    eve_measured_bits = measure_qubits(alice_bits, alice_bases, eve_bases)

    return eve_measured_bits, eve_bases

def check_for_eavesdropper(sifted_key_alice, sifted_key_bob, sample_size = None):
    if sample_size is None:
        sample_size = len(sifted_key_alice) // 10
    if len(sifted_key_alice) < sample_size:
        print("Not enough bits to sample.")
        return False

    sample_alice = sifted_key_alice[:sample_size]
    sample_bob = sifted_key_bob[:sample_size]

    errors = 0
    for a, b in zip(sample_alice, sample_bob):
        if a != b:
            errors += 1

    error_rate = errors / sample_size

    if error_rate == 0:
        print("Secure connection established!")
        print(f"Sample Check: {errors} errors found in {sample_size} bits.")
        return True, sifted_key_alice[sample_size:]
    else:
        print("Errors detected! Potential eavesdropper.")
        print(f"Sample Check: {errors} errors found in {sample_size} bits.")
        print(f"Error Rate: {error_rate:.2%}")
        return False, []

def visualize_errors(alice_key, bob_key, limit=20):
    print(f"\n--- Key Comparison (First {limit} bits) ---")
    print(f"Alice: {alice_key[:limit]}")
    print(f"Bob:   {bob_key[:limit]}")

    diff_str = ""
    for a, b in zip(alice_key[:limit], bob_key[:limit]):
        if a == b:
            diff_str += "   "
        else:
            diff_str += " ^ "

    print(f"Diff:  {diff_str}")

# --- Main Execution ---
NUM_BITS = 1024
print(f"--- Starting BB84 Simulation with {NUM_BITS} Qubits ---")

alice_bits = generate_random_bits(NUM_BITS)
alice_bases = generate_random_bits(NUM_BITS)
bob_bases = generate_random_bits(NUM_BITS)

eavesdropper_present = input("Do you want Eve to intercept? (y/n): ").lower() == 'y'

if eavesdropper_present:
    print("------Eve is intercepting the line!------")
    eve_bits, eve_bases = intercept_qubits(alice_bits, alice_bases)
    bob_measured_bits = measure_qubits(eve_bits, eve_bases, bob_bases)
else:
    print("Channel is secure. Direct transmission.")
    bob_measured_bits = measure_qubits(alice_bits, alice_bases, bob_bases)

bob_key = sift_keys(alice_bases, bob_bases, bob_measured_bits)
alice_key = sift_keys(alice_bases, bob_bases, alice_bits)

print(f"\nOriginal bits sent: {len(alice_bits)}")
print(f"Sifted key length:  {len(alice_key)}")

visualize_errors(alice_key, bob_key)
secure, final_key = check_for_eavesdropper(alice_key, bob_key)

if secure:
    print(f"\nFinal Shared Secret Key (first 10 bits): {final_key[:10]}")
    print(f"Key Length: {len(final_key)}")
