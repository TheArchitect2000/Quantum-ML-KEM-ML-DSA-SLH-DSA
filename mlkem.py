import random

# SUPER SIMPLE SETTINGS
N = 2  # We'll use degree-1 polynomials (just ax + b) 2 here meaning 2 coefficient
Q = 17 # Small modulus so we can see the numbers
ETA = 1 # Only use -1, 0, 1 as noise

# Polynomial helpers (treat them as lists)
def poly_add(p1, p2):
    return [(a+b) % Q for a,b in zip(p1,p2)]

def poly_sub(p1, p2):
    return [(a-b) % Q for a,b in zip(p1,p2)]

def poly_mul(p1, p2):
    # Simple multiplication for degree-1 polynomials
    a0, a1 = p1
    b0, b1 = p2
    return [
        (a0*b0 - a1*b1) % Q,  # Because x² = -1 in our system
        (a0*b1 + a1*b0) % Q
    ]

# Generate random polynomial with small coefficients
def make_noise():
    return [random.randint(-ETA, ETA) % Q for _ in range(N)]

# Generate random polynomial
def make_poly():
    return [random.randint(0, Q-1) for _ in range(N)]

# KEY GENERATION (Alice makes her public/secret keys)
def make_keys():
    # Alice's secret (two small noisy polynomials)
    s0 = make_noise()
    s1 = make_noise()
    secret_key = [s0, s1]
    
    # Public matrix A (random polynomials)
    A00 = make_poly()
    A01 = make_poly()
    A10 = make_poly()
    A11 = make_poly()
    
    # Compute b = A*s + e
    e0 = make_noise()
    e1 = make_noise()
    
    b0 = poly_add(poly_mul(A00, s0), poly_mul(A01, s1))
    b0 = poly_add(b0, e0)
    
    b1 = poly_add(poly_mul(A10, s0), poly_mul(A11, s1))
    b1 = poly_add(b1, e1)
    
    public_key = {
        'A': [[A00, A01], [A10, A11]],
        'b': [b0, b1]
    }
    
    return public_key, secret_key

# ENCRYPTION (Bob uses Alice's public key)
def encrypt(pk):
    # Bob's random small polynomials
    r0 = make_noise()
    r1 = make_noise()
    
    # Small noise polynomials
    e1_0 = make_noise()
    e1_1 = make_noise()
    e2 = make_noise()
    
    # Compute u = A*r + e1
    u0 = poly_add(poly_mul(pk['A'][0][0], r0), poly_mul(pk['A'][0][1], r1))
    u0 = poly_add(u0, e1_0)
    
    u1 = poly_add(poly_mul(pk['A'][1][0], r0), poly_mul(pk['A'][1][1], r1))
    u1 = poly_add(u1, e1_1)
    
    # Compute v = b*r + e2
    v_part = poly_add(poly_mul(pk['b'][0], r0), poly_mul(pk['b'][1], r1))
    v = poly_add(v_part, e2)
    
    # Shared secret is just whether coefficients are > Q/2
    secret = [1 if x > Q//2 else 0 for x in v]
    
    ciphertext = {
        'u': [u0, u1],
        'v': v
    }
    
    return ciphertext, secret

# DECRYPTION (Alice uses her secret key)
def decrypt(ct, sk):
    # Compute m = u*s
    m_part = poly_add(poly_mul(ct['u'][0], sk[0]), poly_mul(ct['u'][1], sk[1]))
    
    # Compute v - m
    diff = poly_sub(ct['v'], m_part)
    
    # Get same secret by checking same thresholds
    secret = [1 if x > Q//2 else 0 for x in diff]
    
    return secret

# LET'S RUN IT!
print("=== SUPER SIMPLE ML-KEM ===")
print(f"Using polynomials of degree 1 (N={N})")
print(f"Modulus Q={Q}, Noise ETA={ETA}\n")

# Alice makes her keys
pk, sk = make_keys()
print("Alice's Public Key:", pk)
print("Alice's Secret Key:", sk)

# Bob sends a message
ct, bob_secret = encrypt(pk)
print("\nBob's Ciphertext:", ct)
print("Bob's Shared Secret:", bob_secret)

# Alice decrypts
alice_secret = decrypt(ct, sk)
print("\nAlice's Shared Secret:", alice_secret)

# Did they match?
print("\nSUCCESS?", bob_secret == alice_secret)