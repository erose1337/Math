# "Subset Inner Product Problem"
# ====================
# - Public information: A set of n elements: a, b, c, ...,
# - F:
#
#         select a random vector X of length k using elements of the set
#         select a random vector Y of length k using elements of the set
#         output XY
#
#     (Where `XY` denotes the dot product (or inner product) of X and Y)
# - How large should `n` and `k` be?
#     - if `k` is too large, repeats will be selected from the set
#     - log2(k) < log2(n) / 2 == k < sqrt(n)
#       - Alternatively:
#           - rejection sampling can ensure no duplicates
#           - Pick a random binary vector of length n and weight k
#           - the "random vector" is the k selected entries from the set
#           - guarantees no duplicates; can use higher weight subsets
#     - how large should 'n' be?
#        - surely the problem is no easier than a subset-sum problem
#           - n = 1024 for subset-sum problem should provide approximately 128-bit security (post-quantum)
from utilities import random_integer

SECURITY_LEVEL = 32

def generate_parameters(security_level=SECURITY_LEVEL):
    n = 256
    parameters = {'n' : n, 'k' : 128,
                  "set" :[random_integer(SECURITY_LEVEL) for count in range(n)]}
    return parameters

PARAMETERS = generate_parameters(SECURITY_LEVEL)

def random_vector(parameters=PARAMETERS):
    n = parameters['n']; k = parameters['k']; _set = parameters["set"]
    # two options for how-to
    # 1. rejection sampling
    #       - pick random indices, and re-draw if a repeat index is selected
    #       - vectors produced this way can/will be in a different order each time the same subset of elements is selected
    #           - could sort the result if consistent ordering is desirable
    # 2. generate random bit string of length n and weight k
    #       - pick elements from set according to 1s in the bit string
    #       - vectors produced this way will always be in the same order if the same indices are selected
    bits = ([0] * n) + [0] # extra bit facilitates an attempt to reduce timing variations
    output = []
    _ = []
    _2 = k
    while k:
        index = random_integer(4) % n # possibly biased
        # not constant time?
        if bits[index]:
            bits[-1] = 1
            _.append(_set[index])
            _2 -= 1
        else:
            bits[index] = 1
            output.append(_set[index])
            k -= 1
    return output

def generate_vectors(parameters=PARAMETERS):
    return random_vector(parameters), random_vector(parameters)

def generate_point(vector1, vector2):
    return sum(vector_i * vector2[i] for i, vector_i in enumerate(vector1))
