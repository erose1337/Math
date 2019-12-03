import random
print("Warning: apencrypt.py uses insecure `random` module and is not intended for serious use.")

from linearalgebra import *
from utilities import is_prime, random_integer

SECURITY_LEVEL = 32

def generate_p(p_size):
    p = 2 ** (p_size * 8)
    offset = 1
    while not is_prime(p + offset):
        offset += 2
    return p + offset

def performance_information(p, p_size, nmin=2, nmax=64, kmin=1, kmax=64):
    # find the value of n, k such that the size of G and/or the key are minimized
    # choose to use the smallest n! ** k >= p to come closest to a 1-to-1 mapping between permutations and elements of p

    # find the value of n, k such that the cost of evaluating F is minimized
    # cost to evaluate F determined by:
    #   - number of matrix multiplications (determined by k, the number of shuffles)
    #   - width of each matrix (determined by n)
    #   - cost of multiplication
    #       - number of multiplications:
    #           - n * k for the matrix mul with NxN permutation matrix (scalar mult with 0 will be considered free)
    #           - n * (k - 1) for k >= 1 from the entrywise products used to combine the k shuffled vectors
    #           - n from computing the dot product with the shuffled vector at the end
    #           - n * k + n * (k - 1) + n
    #           - 2 * n * k multiplictions used to evaluate F
    factorialn = 1
    output = dict((n, dict()) for n in range(nmin, nmax))
    for n in range(nmin, nmax):
        factorialn *= n
        for k in range(kmin, kmax):
            if k > n / 2:
                break
            if factorialn ** k >= p:
                G_size = (n ** 2) * k   # n ** 2 is number of bits used in an NxN permutation matrix, and there are k of them
                k_size = 8 * p_size * n
                nmuls = 2 * n * k
                output[n][k] = (k_size, G_size, nmuls)
                print("n: {}; k: {}; Key size: {}; G size: {}; #Muls: {}".format(n, k, k_size, G_size, nmuls))
                break

def generate_parameters(security_level=SECURITY_LEVEL):
    p_size = security_level; p = generate_p(p_size);
    print p
    #performance_information(p, p_size); raise SystemExit()
    return {"p_size" : security_level, 'p' : p, 'n' : 16, 'k' : 6}

PARAMETERS = generate_parameters(SECURITY_LEVEL)

def generate_permutation_matrix(parameters=PARAMETERS):
    n = parameters['n']
    key = [[0 for count in range(n)] for _ in range(n)]
    for i in range(n):
        key[i][i] = 1
    random.shuffle(key) # obviously insecure, testing purposes etc
    return key

def generate_permutation_tensor(parameters=PARAMETERS):
    return [generate_permutation_matrix(parameters) for count in range(parameters['k'])]

def generate_key_vector(parameters=PARAMETERS):
    return [random_integer(parameters["p_size"]) for count in range(PARAMETERS['n'])]

def generate_seed(parameters=PARAMETERS):
    return generate_permutation_tensor(parameters)

def generate_key(parameters=PARAMETERS):
    return generate_key_vector(parameters)

def F(T, k, dot=dotproduct):
    v = reduce(add_vector, [mmul(M, k) for M in T])
    return dot(k, v)

def encrypt(message, key, dot=dotproduct, parameters=PARAMETERS):
    G = generate_seed(parameters)
    return G, (message + F(G, key)) % parameters['p']

def decrypt(cryptogram, key, dot=dotproduct, parameters=PARAMETERS):
    G, ciphertext = cryptogram
    return (ciphertext - F(G, key)) % parameters['p']

def add_cryptogram(c1, c2):
    return (add_tensor(c1[0], c2[0]), c1[1] + c2[1])

def scale_cryptogram(c1, s, parameters=PARAMETERS):
    return scale_tensor(c1[0], s), (c1[1] * s) % PARAMETERS['p']

def test_F():
    from utilities import random_integer
    from copy import deepcopy
    n = PARAMETERS['n']
    b = dotproduct2

    for count in range(256):
        K = generate_key()
        J = generate_key()
        KJ = add_matrix(K, J)

        # bits
        v = [random_integer(1) % 2 for _ in range(n)]
        KJ = add_matrix(K, J)
        assert F(K, v, b) ^ F(J, v, b) == F(KJ, v, b), (count, F(K, v, b), F(J, v, b), F(KJ, v, b))

        y = random_integer(1) % 2
        v2 = scale_vector(v, y)
        assert y * y * F(K, v, b) == F(K, v2, b), (count, y * y * F(K, v, b), F(K, v2, b))

        K2 = scale_matrix(K, y)
        assert y * F(K, v, b) == F(K2, v, b)

        # integers
        v = [random_integer(1) for _ in range(n)]
        assert F(K, v) + F(J, v) == F(KJ, v), (count, F(K, v), F(J, v), F(KJ, v))

        y = random_integer(1)
        v2 = scale_vector(v, y)
        assert y * y * F(K, v) == F(K, v2), (count, y * y * F(K, v), F(K, v2))

        K2 = scale_matrix(K, y)
        assert y * F(K, v) == F(K2, v)
        assert y * y * F(K, v) == F(scale_matrix(K2, y), v)

def test_encrypt_decrypt():
    for count in range(1000):
        key = generate_key()
        c1 = encrypt(1, key)
        c2 = encrypt(2, key)
        c3 = add_cryptogram(c1, c2)
        assert decrypt(c1, key) == 1
        assert decrypt(c2, key) == 2
        assert decrypt(c3, key) == 3

        r1, r2 = [random_integer(PARAMETERS["p_size"]) for _ in range(2)]
        c1 = encrypt(r1, key); c2 = encrypt(r2, key); c3 = add_cryptogram(c1, c2)
        assert decrypt(c1, key) == r1
        assert decrypt(c2, key) == r2
        assert decrypt(c3, key) == (r1 + r2) % PARAMETERS['p']

        scaledc1 = scale_cryptogram(encrypt(1, key), r1)
        assert decrypt(scaledc1, key) == r1

if __name__ == "__main__":
    #test_F()
    #test2()
    test_encrypt_decrypt()
