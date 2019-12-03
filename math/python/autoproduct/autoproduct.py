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

def generate_key(parameters=PARAMETERS):
    n = parameters['n']
    key = [[0 for count in range(n)] for _ in range(n)]
    for i in range(n):
        key[i][i] = 1
    random.shuffle(key) # obviously insecure, testing purposes etc
    return key

#def generate_key(parameters=PARAMETERS):
#    n = parameters['n']; size = parameters["s_size"]
#    key = [[0 for count in range(n)] for _ in range(n)]
#    for i in range(n):
#        key[i][i] = random_integer(size)
#    random.shuffle(key) # obviously insecure, testing purposes etc
#    return key

def generate_vector(parameters=PARAMETERS):
    return [random_integer(parameters["p_size"]) for count in range(PARAMETERS['n'])]

def F(k, v, dot=dotproduct):
    x = mmul(k, v, dot) # shuffle
    return dot(v, x) # dot product

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

def test2():
    from utilities import random_integer
    def tobits(x):
        return [int(item) for item in format(x, 'b').zfill(32)]
    for counter in range(256):
        X = generate_key(); Y = generate_key();
        g = [random_integer(2) >> 2 for count in range(32)]
        pubx = tobits(F(X, g)); puby = tobits(F(Y, g))
        while len(pubx) != 32 or len(puby) != 32:
            g = [random_integer(2) >> 2 for count in range(32)]
            pubx = tobits(F(X, g)); puby = tobits(F(Y, g))
        assert F(X, puby, dotproduct2) == F(Y, pubx, dotproduct2), counter
        # relationship does not hold

def test3():
    from utilities import random_integer
    M = generate_key(); one = M[0].index(1)
    G = generate_vector()#[random_integer(32) for count in range(PARAMETERS['n'])]
    x = random_integer(PARAMETERS["p_size"]); y = random_integer(PARAMETERS["p_size"]);
    e = random_integer(36); q = random_integer(36)
    Mx = scale_matrix(M, x); My = scale_matrix(M, y)
    Mx[0][one] += e; My[0][one] += q
    pubx = F(Mx, G); puby = F(My, G)
    sharex = e * puby
    sharey = q * pubx
    print format(sharex & sharey, 'b').zfill((140) * 8)[:160]
    print
    print format(sharex, 'b').zfill((140) * 8)[:160]
    print
    def product(items):
        output = 1
        for item in items:
            output *= item
        return output
    print format(pubx * puby / product(G[:-2]), 'b').zfill((140) * 8)[:160]
    from math import log

if __name__ == "__main__":
    test_F()
    #test2()
    test3()
