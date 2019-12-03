import copy
import random
print("Warning: autoproduct.py uses insecure `random` module and is not intended for serious use.")

from linearalgebra import *
from utilities import is_prime, random_integer
SECURITY_LEVEL = 32

def determine_n_size(p_size_in_bits, s_size_in_bits):
    """ Determines what size n should be, based on how large the modulus p and any scalars s are.

            n! >= p
            n! >= 2^(log2(p) - n*log2(s))
        > "There's no way to recover information equivalent to a random choice from 209! possibilities when you only have 1288 bits of information."
        > "So there can be no method that recovers an equivalent key"
        s_size_in_bits indicates the amount of size taken by the scalar variables *after* the autoproduct evaluation.
            - this is twice the "s_size" found in the parameters"""
    accumulator = 1;  n = 1
    while True:
        p = 2 ** (p_size_in_bits - (n * s_size_in_bits))
        if accumulator >= p: return n
        else: n += 1; accumulator *= n

def generate_p(p_size):
    p = 2 ** (p_size * 8)
    offset = 1
    while not is_prime(p + offset):
        offset += 2
    return p + offset

def generate_parameters(security_level=SECURITY_LEVEL):
    p_size = security_level; s_size = 4 # s_size = 4 is just an initial guess
    n = determine_n_size(p_size * 8, s_size * 8 * 2)
    p = generate_p(p_size)
    return {"p_size" : security_level, "s_size" : s_size, 'n' : n, 'p' : p}

PARAMETERS = generate_parameters(SECURITY_LEVEL)
IDENTITY_MATRIX = [[0 for _ in range(PARAMETERS['n'])] for _ in range(PARAMETERS['n'])]
for i in range(PARAMETERS['n']):
    IDENTITY_MATRIX[i][i] = 1

def generate_tensor(parameters=PARAMETERS, identity_matrix=IDENTITY_MATRIX):
    n = parameters['n']
    T = []
    for _ in range(n):
        M = copy.deepcopy(identity_matrix)
        random.shuffle(M) # obviously insecure, testing purposes etc
        T.append(M)
    return T

def generate_vector(parameters=PARAMETERS):
    return [random_integer(parameters["p_size"]) for count in range(PARAMETERS['n'])]

def F(T, v, dot=dotproduct): # outputs a vector
    return [dot(mmul(M, v, dot), v) for M in T]

def G(T, v, dot=dotproduct):
    k = reduce(entrywise_productv, [mmul(M, v, dot) for M in T])
    return dot(v, k)

def test_F():
    from utilities import random_integer
    from copy import deepcopy
    n = PARAMETERS['n']
    b = dotproduct2
    for count in range(256):
        K = generate_tensor()
        J = generate_tensor()
        KJ = add_tensor(K, J)

        # bits
        v = [random_integer(1) % 2 for _ in range(n)]
        FKv = F(K, v, b)
        FJv = F(J, v, b)
        FKJv = F(KJ, v, b)
        assert xor_vector(FKv, FJv) == FKJv, (count, F(K, v, b), F(J, v, b), F(KJ, v, b))

        y = random_integer(1) % 2
        v2 = scale_vector(v, y)
        assert scale_vector(F(K, v, b), y * y) == F(K, v2, b), (count, y * y * F(K, v, b), F(K, v2, b))

        K2 = scale_tensor(K, y)
        assert scale_vector(F(K, v, b), y) == F(K2, v, b)

        # integers
        v = [random_integer(1) for _ in range(n)]
        assert add_vector(F(K, v), F(J, v)) == F(KJ, v), (count, F(K, v), F(J, v), F(KJ, v))

        y = random_integer(1)
        v2 = scale_vector(v, y)
        assert scale_vector(F(K, v), y * y) == F(K, v2), (count, scale_vector(F(K, v), y * y), F(K, v2))

        K2 = scale_tensor(K, y)
        assert scale_vector(F(K, v), y) == F(K2, v)
        assert scale_vector(F(K, v), y * y) == F(scale_tensor(K2, y), v)

def test_G():
    T = generate_tensor()
    v = generate_vector()
    raise NotImplementedError()

def test2():
    from utilities import random_integer
    G = generate_tensor()
    for counter in range(256):
        x = generate_vector(); y = generate_vector()
        pubx = F(G, x); puby = F(G, y)
        dotproduct(pubx, y) == dotproduct(puby, x)

if __name__ == "__main__":
    test_F()
    test2()
