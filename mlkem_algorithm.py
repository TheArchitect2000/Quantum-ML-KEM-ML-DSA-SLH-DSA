from hashlib import sha3_256

# --------------------------
# Parameters
# --------------------------
n = 4  # Degree of polynomials (small for demonstration)
q = 17  # Small modulus
k = 2  # Module rank (2 polynomials per vector)

# --------------------------
# Polynomial Operations
# --------------------------
def poly_add(a, b):
    """Add two polynomials modulo q"""
    return [(x + y) % q for x, y in zip(a, b)]


def poly_mul(a, b):
    """Multiply two polynomials modulo (X^n + 1) and q"""
    c = [0] * n
    for i in range(n):
        for j in range(n):
            c[(i + j) % n] = (c[(i + j) % n] + a[i] * b[j]) % q
    return c

# --------------------------
# Key Generation
# --------------------------
def keygen():
    # Static example matrices
    A = [
        [[1, 0, 0, 0], [2, 1, 3, 0]],
        [[0, 1, 2, 0], [1, 1, 1, 1]],
    ]
    s = [[1, -1, 0, 1], [0, 1, -1, 0]]
    e = [[1, 0, -1, 1], [0, 1, 0, -1]]

    t = []
    for i in range(k):
        ti = [0] * n
        for j in range(k):
            ti = poly_add(ti, poly_mul(A[i][j], s[j]))
        ti = poly_add(ti, e[i])
        t.append(ti)

    return (A, t), s

# --------------------------
# Encapsulation
# --------------------------
def encapsulate(pk):
    A, t = pk
    r = [[1, -1, 0, 0], [0, 1, -1, 0]]
    e1 = [[0, 1, 0, -1], [1, 0, 0, 0]]
    e2 = [1, 0, 1, 0]
    m = [1, 0, 1, 0]  # Message to encrypt

    # Compute u = A^T * r + e1
    u = []
    for i in range(k):
        ui = [0] * n
        for j in range(k):
            ui = poly_add(ui, poly_mul(A[j][i], r[j]))
        ui = poly_add(ui, e1[i])
        u.append(ui)

    # Compute v = t^T * r + e2 + m
    v = [0] * n
    for i in range(k):
        v = poly_add(v, poly_mul(t[i], r[i]))
    v = poly_add(v, e2)
    v = poly_add(v, m)

    # Derive shared secret
    m_bytes = bytes(m)
    shared_secret = sha3_256(m_bytes).hexdigest()

    return (u, v), shared_secret

# --------------------------
# Decapsulation
# --------------------------
def decapsulate(sk, ct):
    u, v = ct
    s = sk

    # Compute v' = u^T * s
    vp = [0] * n
    for i in range(k):
        vp = poly_add(vp, poly_mul(u[i], s[i]))

    # Recover m' = v - v'
    m_recovered = [(vi - vpi) % q for vi, vpi in zip(v, vp)]

    # Derive shared secret
    m_bytes = bytes(m_recovered)
    shared_secret = sha3_256(m_bytes).hexdigest()

    return shared_secret

# --------------------------
# Main Testing
# --------------------------
if __name__ == "__main__":
    print("🔐 Starting ML-KEM Simulation\n")

    # Key Generation
    pk, sk = keygen()
    print("✅ Keys generated")

    # Encapsulation
    ct, shared_secret_enc = encapsulate(pk)
    print("📦 Encapsulation complete")

    # Decapsulation
    shared_secret_dec = decapsulate(sk, ct)
    print("🔓 Decapsulation complete")

    # Result
    print("\nShared Secret (Encapsulation):", shared_secret_enc)
    print("Shared Secret (Decapsulation):", shared_secret_dec)
    print("\n✅ Secrets Match:", shared_secret_enc == shared_secret_dec)
