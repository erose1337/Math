import random
print("Warning: monoproduct uses the insecure `random` module")

from utilities import random_integer
from linearalgebra import dotproduct, mmul, add_vector

Q = 2 ** 1024
N = 16
K = 1024
R_SIZE = 128

def random_vector(n, q=Q, r_size=R_SIZE):
    return [random_integer(r_size) % q for i in range(n)]

G = random_vector(N, Q, R_SIZE)

def random_permutation_matrix(n):
    matrix = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    random.shuffle(matrix)
    return matrix

def compress(vector, q=Q):
    degree = len(vector)
    found = False
    for scalar in vector:
        for scalar2 in vector:
            if pow(scalar, degree, q) == scalar2:
                found = True
                break
        if found:
            break
    else:
        raise ValueError("No relation found")

    # alternatively: return scalar, mmul(inverse_permutation, vector)
    matrix = [[0] * degree for count in range(degree)]
    for i in range(degree):
        si = vector[i]
        for j in range(1, degree + 1):
            if pow(scalar, j, q) == si:
                matrix[i][j - 1] = 1
                break
    return scalar, matrix

def decompress(scalar, k, n, q=Q):
    vector = [pow(scalar, i, q) for i in range(1, n + 1)]
    return mmul(k, vector)

def f(a, v, q=Q):
    return dotproduct(a, v) % q

def generate_private_key(size=R_SIZE, n=N, k=K, q=Q):
    private_key = []
    for count in range(k):
        scalar = random_integer(size)
        k = random_permutation_matrix(n)
        private_key.append(decompress(scalar, k, n, q))
    return private_key

def generate_public_key(private_key, g=G, q=Q):
    return [f(g, vector) for vector in private_key]

def generate_keypair():
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    return public_key, private_key

def sign(private_key, r, n=N, k=K, q=Q):
    signature = [0] * n
    for i in range(k):
        if r & 1:
            assert len(signature) == len(private_key[i])
            signature = add_vector(signature, private_key[i])
        r >>= 1
    return [x % q for x in signature]

def decompress_and_sign(private_key, r, n=N, k=K, q=Q):
    signature = [0] * n
    for i in range(k):
        if r & 1:
            signature = add_vector(signature, decompress(*(private_key[i] + (n, q, ))))
        r >>= 1
    return [x % q for x in signature]

def verify(public_key, r, signature, n=16, k=K, g=G, q=Q):
    #public_key, r, signature, n, k, g, q = sanitize_verify(public_key, r, signature, n, k, g, q)
    verifier = 0
    for i in range(k):
        if r & 1:
            verifier = (verifier + public_key[i]) % q
        r >>= 1
    assert len(g) == len(signature)
    if f(g, signature) == verifier:
        return True
    else:
        return False

def test_f():
    from linearalgebra import scale_vector
    n = N
    for count in range(256):
        a = random_vector(n)
        xs = random_integer(1)
        xk = random_permutation_matrix(n)
        xv = decompress(xs, xk, n)
        fx = f(a, xv)

        ys = random_integer(1)
        yk = random_permutation_matrix(n)
        yv = decompress(ys, yk, n)
        fy = f(a, yv)

        xyv = [(xv[i] + yv[i]) % Q for i in range(n)]
        fxy1 = f(a, xyv)
        fxy2 = (fx + fy) % Q
        assert fxy1 == fxy2

        s = random_integer(1)
        assert (s * fx) % Q == f(a, scale_vector(xv, s))

def test_sign_verify():
    test_size = 1024
    public, private = generate_keypair()
    compressed = [compress(key) for key in private]

    r = random_integer(R_SIZE)
    signature = sign(private, r)
    assert verify(public, r, signature)

    signature2 = decompress_and_sign(compressed, r)
    assert signature2 == signature

    from timeit import default_timer as timestamp
    before = timestamp()
    for count in range(test_size):
        r = random_integer(R_SIZE)
        signature = sign(private, r)
        assert verify(public, r, signature)

        #r2 = random_integer(R_SIZE)
        #signature2 = decompress_and_sign(compressed, r2)
        #assert verify(public, r2, signature2)
    after = timestamp()

    from math import log, factorial
    print("sign/verify test complete")
    public_size = log(Q, 2) * N
    private_size = log(Q, 2) * K * N
    compressed_size = log(Q, 2) + log(factorial(N), 2)
    signature_size = log(Q, 2) * N
    print("Public key size : {} bits ({} bytes)".format(public_size, public_size / 8))
    print("Private key size: {} bits ({} bytes)".format(private_size, private_size / 8))
    print("----> Compressed size: {} bits ({} bytes)".format(compressed_size, compressed_size / 8))
    print("Signaure size   : {} bits ({} bytes)".format(signature_size, signature_size / 8))
    print("Time taken to produce {} signatures: {} seconds".format(test_size, after - before))



def test_compress_decompress():
    scalar = random_integer(R_SIZE)
    matrix = random_permutation_matrix(N)
    vector = decompress(scalar, matrix, N)
    _scalar, _matrix = compress(vector)
    #print("Scalar: {}".format(scalar))
    #print("Vector: {}".format(vector))
    #print("Matrix:\n{}".format('\n'.join(str(item) for item in matrix)))
    #print("_Matrix:\n{}".format('\n'.join(str(item) for item in _matrix)))
    assert _scalar == scalar
    assert _matrix == matrix

if __name__ == "__main__":
    test_f()
    test_sign_verify()
    test_compress_decompress()
