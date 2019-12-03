# keep matrix and vector secret
# include third argument for secret random short vector
#   - what if the vector is chosen as a random permutation of a public set of short vectors?
#       - implies the set of the possible values for all variables is known
#       - the mapping between variable names and values is the secret
#           - how many possible combinations of variable name: value pairs are there?
#               - n*(n + 1) / 2  approx n**2, where n = number of variable names (or number of values, assuming both are the same)
#                   - what if they are not the same? e.g. the same value appears twice?
#       - provides only a quadratic advantage
#
# antidot product
# - degree = dimension
#
#     a b c d
#     c b d a
#               (a + c)(b + b)(c + d)(d + a)
#               (2ab + 2bc)(c + d)(d + a)
#               (2abc + 2abd + 2bcc + 2bcd)(d + a)
#                2abcd + 2aabc + 2abdd + 2aabd + 2bccd + 2abcc + 2bcdd + 2bcda
#                2(abcd + aabc + abdd + aabd + bccd + abcc + bcdd + bcda)
#
#    aw bx cy dz        apply short vector first...
#    cy bx dz aw
#                (aw + cy)(bx + bx)(cy + dz)(dz + aw)
#                (aw + cy)2bx
#                (2bxaw + 2bxcy)(cy + dz)(dz + aw)
#                (2bxawcy + 2bxawdz + 2bxcycy + 2bxcydz)(dz + aw)
#      2bxawcydz + 2bxawcyaw + 2bxawdzdz + 2bxawdzaw + 2bxcycydz +2bxcycyaw + 2bxcydzdz + 2bxcydzaw
#     2(abcdwxyz +  aabcwwxy +  abddwxzz +  aabdwwxz +  bccdxyyz + abccwxxy +  bcddxyzz +  abcdwxyz)
#
#   the structure of the equation is determined by the permutation matrix
#       - the permutation matrix defines a multivariate polynomial
#   the key (short vector) gives knowledge of the factorization of the output


import operator
import random
print("Warning: autoproduct2.py uses insecure `random` module and is not intended for serious use.")

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
    s_size = 2; # security_level / n
    #performance_information(p, p_size); raise SystemExit()
    return {"p_size" : security_level, 'p' : p, 'n' : 16, 'k' : 6, "s_size" : s_size}

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

def generate_random_vector(parameters=PARAMETERS):
    return [random_integer(parameters["p_size"]) for count in range(parameters['n'])]

def generate_random_short_vector(parameters=PARAMETERS):
    return [random_integer(parameters["s_size"]) for count in range(parameters['n'])]

def generate_seed(parameters=PARAMETERS):
    return generate_permutation_tensor(parameters), generate_random_vector(parameters)

def generate_key(parameters=PARAMETERS):
    return generate_random_short_vector(parameters)

def antidot(v1, v2):
    return reduce(operator.mul, (v1[i] + v2[i] for i in range(len(v1))))

def F(seed, k):
    T, g = seed
    gk = entrywise_productv(g, k)
    x = [mmul(M, gk) for M in T][0] # remove [0] when higher degree functionality is restored
    #v = reduce(add_vector, [mmul(M, k) for M in T])
    return antidot(gk, x)

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
        g1, g2 = generate_seed(), generate_seed()
        key1, key2 = generate_key(), generate_key()
        out1 = F(g1, key1); out2 = F(g1, key2)
        test1 = reduce(operator.mul, key1); test2 = reduce(operator.mul, key2)
        print (out1 * test2) == (out2 * test1)

        #out3 = out1 + out2; key3 = add_vector(key1, key2)
        #_out3 = F(g1, key3)
        #print _out3 == out3#, (out3, _out3)

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
    test_F()
    #test2()
    #test_encrypt_decrypt()
