"""
ML-KEM Python Implementation
Author: Parsa
Assignment: Quantum Shield - ML-KEM Implementation
"""

# ============================
# Import Required Libraries
# ============================
import numpy as np  # for matrix and polynomial operations
import hashlib      # for hashing (if needed later)
import os           # for random key generation

# ============================
# Step 1: Parameter Definitions
# ============================

# Define constants and parameters for ML-KEM
# (These values will be placeholders; we will refine them later)
N = 256           # degree of polynomials
q = 3329          # modulus (a prime number used in lattice cryptography)
seed_size = 32    # seed length in bytes

# ============================
# Step 2: Key Generation
# ============================

def keygen():
    """
    Generate a public and private key pair.
    """
    # Generate a random matrix A (N x N) with elements in range [0, q)
    A = np.random.randint(0, q, size=(N, N))

    # Generate secret s and error e (random small values)
    s = np.random.randint(0, 3, size=(N, 1))  # secret key vector
    e = np.random.randint(0, 3, size=(N, 1))  # error vector

    # Compute b = A * s + e mod q
    b = (np.matmul(A, s) + e) % q

    # Public key = (A, b), Private key = s
    public_key = (A, b)
    private_key = s

    return public_key, private_key



# ============================
# Step 3: Encapsulation
# ============================


def encapsulate(public_key):
    """
    Given a public key, generate a ciphertext and shared secret.
    """
    A, b = public_key

    # Step 1: Random message m and ephemeral secret r
    m = np.random.randint(0, 2, size=(N, 1))  # message (random bits)
    r = np.random.randint(0, 3, size=(N, 1))  # ephemeral secret
    e1 = np.random.randint(0, 3, size=(N, 1))  # error
    e2 = np.random.randint(0, 3, size=(1, 1))  # small noise

    # Step 2: Compute u = A * r + e1 mod q
    u = (np.matmul(A, r) + e1) % q

    # Step 3: Compute v = bᵗ * r + e2 + m mod q
    v = (np.matmul(b.T, r) + e2 + m) % q

    # Step 4: Combine u and v into ciphertext
    ciphertext = (u, v)

    # Step 5: Derive shared secret (e.g., hash of message m)
    m_bytes = m.astype(np.uint8).tobytes()
    shared_secret = hashlib.sha256(m_bytes).hexdigest()

    return ciphertext, shared_secret

# ============================
# Step 4: Decapsulation
# ============================

def decapsulate(ciphertext, private_key):
    """
    Given a ciphertext and a private key, recover the shared secret.
    """
    u, v = ciphertext
    s = private_key

    # Step 1: Compute v' = uᵗ * s mod q
    v_prime = np.matmul(u.T, s) % q

    # Step 2: Recover m = (v - v') mod q
    m_recovered = (v - v_prime.T) % q

    # Optional: Round values to bits
    m_bits = np.round(m_recovered % 2).astype(np.uint8)

    # Step 3: Derive shared secret
    m_bytes = m_bits.tobytes()
    shared_secret = hashlib.sha256(m_bytes).hexdigest()

    return shared_secret

# ============================
# Step 5: Test the Algorithm
# ============================

def main():
    print("🔐 ML-KEM Key Encapsulation Test")

    # Key Generation
    pk, sk = keygen()
    print("\n✅ Keys generated:")
    print("Public Key (A shape):", pk[0].shape)
    print("Public Key (b shape):", pk[1].shape)
    print("Private Key (s shape):", sk.shape)


    # Encapsulation
    ct, ss1 = encapsulate(pk)
    print("\n📦 Encapsulation:")
    print("Ciphertext:", ct)
    print("Shared Secret (Sender):", ss1)

    # Decapsulation
    ss2 = decapsulate(ct, sk)
    print("\n🔓 Decapsulation:")
    print("Shared Secret (Receiver):", ss2)

    # Verification
    print("\n✅ Keys Match:", ss1 == ss2)


if __name__ == "__main__":
    main()
