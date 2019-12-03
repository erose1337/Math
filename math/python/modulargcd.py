# x(yr + m) * x(yr + m)
# xx(yr + m)(yr + m)
# xx yyrr + yrm + yrm + mm
# xxyyrr + 2yrm + mm
# (xxyyrr + 2yrm + mm)(xyr + xm)
#
# 1: 2
# 2: 4
# 3 : 6
from math import log

from utilities import random_integer, is_prime, modular_inverse, isqrt

SECURITY_LEVEL = 24
DEFAULT_DEPTH = 2

def _generate_p(p_size):
    p = (2 ** ((8 * p_size) + 1)) + 1
    while not is_prime(p):
        p += 2
    return p

def generate_parameters(security_level=SECURITY_LEVEL, depth=DEFAULT_DEPTH, p=None):
    assert depth == 2
    parameters = {"security_level" : security_level, "depth" : depth}
    # sizes are only set to accomodate the evaluation of a dot product
    # To get the tightest sizes, it is necessary to specify a circuit:
    #   - how many addition gates
    #   - how many multiplication gates
    # y needs to be  n + 1 + (# of carries) bits to be larger than m for depth 1
    #   - + 1 to be larger than n
    # an additional k = log2(# of additions) extra bits to remain larger than n after 2 ** k additions at the current circuit depth
    # for each successive multiplication:
    #   - double the required number of bits
    # for a dot product, y needs to be 2n + 1 bits to be larger where `n` is the size of `m`
    y_size = r_size = security_level
    m_size = security_level / depth
    r_max = (2 ** (8 * y_size)) << 1  # 1 extra bit to ensure y, r, m are always smaller than r_max
    x_size = p_size = (y_size + r_size) * depth
    parameters["m_size"] = m_size; parameters["r_size"] = r_size;
    parameters["y_size"] = y_size; parameters["p_size"] = p_size + 1;
    parameters["x_size"] = x_size; parameters["r_max"] = r_max
    parameters["mask"] = 1 << ((8 * y_size) + 1)
    if p is None:
        parameters['p'] = _generate_p(parameters["p_size"])
    else:
        parameters['p'] = p
        if not is_prime(p):
            raise ValueError("Invalid p; {} is not prime".format(p))
    return parameters

PARAMETERS = generate_parameters(SECURITY_LEVEL, DEFAULT_DEPTH, p=794889263257962974796277498092801308291525640763748664903194643469338087775424965801409745320266996710649718116931109481559848982586784968419475084821084743272680947722675151641735826243378403750534655587182832000457137589153821622877
)
assert SECURITY_LEVEL == 24
#print PARAMETERS['p']
#print
#print PARAMETERS["r_max"]
#raise SystemExit()

def generate_key(parameters=PARAMETERS):
    x = random_integer(parameters["x_size"])
    y = random_integer(parameters["y_size"])
    # fixed upper bit(s) help to ensure that m remains smaller than y
    y |= parameters["mask"]
    d = modular_inverse(x, parameters['p'])
    return x, y, d, pow(d, parameters["depth"], parameters['p'])

def encrypt(m, key, parameters=PARAMETERS):
    p = parameters['p']; depth = parameters["depth"]
    x, y, d, dd = key
    #assert pow(m, depth) < y, (log(m, 2), log(pow(m, depth), 2), log(y, 2))
    #assert 2 * pow(m, depth) < y, (log(m, 2), log(2 * pow(m, depth), 2), log(y, 2))
    r = random_integer(parameters["r_size"]) >> depth
    #assert r < parameters["r_max"]
    #assert r < y
    #assert pow(y, depth) < p, (log(y, 2), log(pow(y, depth), 2), log(p, 2))
    #assert (pow(y, depth) * pow(r, depth)) < p, (log(pow(y, depth) * pow(r, depth), 2), log(y, 2) * depth, log(r, 2) * depth, log(p, 2), depth)
    #assert (pow(y, depth) * pow(r, depth)) + pow(m, depth) < p
    #assert y + ((r * r) + (r * r)) < p
    #assert m < y
    t = (y * r) + m
    #assert t < p
    t = (x * t)
    #assert t > p
    return t % p

def decrypt(c, key, depth=1, parameters=PARAMETERS):
    x, y, d, dd = key
    p = parameters['p']
    return ((pow(d, depth, p) * c) % p) % y

def test_encrypt_decrypt():
    size = SECURITY_LEVEL
    m_size = PARAMETERS["m_size"]
    p = PARAMETERS['p']
    for _outer in range(10):
        for count in range(1024):
            key = generate_key()
            m = 0
            c = encrypt(m, key)
            m2 = decrypt(c, key)
            assert m2 == m, (m2, m)

            magain = decrypt(c + c, key)
            assert magain == 0, (magain, key[1])

            c2 = encrypt(m, key)
            m3 = decrypt(c + c2, key)
            assert m3 == 0, m3
            d = decrypt(encrypt(2, key) + encrypt(2, key), key)
            assert d == 4, d

            m = random_integer(m_size)
            m2 = random_integer(m_size)
            assert m + m2 < key[1]
            c = encrypt(m, key)
            c2 = encrypt(m2, key)
            d = decrypt(c + c2, key)
            assert d == (m + m2), (d, m, m2, m + m2)

            if PARAMETERS["depth"] == 2:
                d = decrypt(pow(c, 2, PARAMETERS['p']), key, depth=2)
                assert d == pow(m, 2)

                d = decrypt(c * c2, key, depth=2)
                assert d == (m * m2), (d, m, m2, (m * m2))

                m3 = random_integer(m_size)
                m4 = random_integer(m_size)
                c3 = encrypt(m3, key)
                c4 = encrypt(m4, key)
                mdot = decrypt((c * c2) + (c3 * c4), key, depth=2)
                assert mdot == ((m * m2) + (m3 * m4))
             #print count
        #print _outer
    from timeit import default_timer as timer
    for name, function in [("encrypt", encrypt), ("decrypt", decrypt)]:
        before = timer()
        for count in range(100000):
            function(0, key)
        after = timer()
        taken = after - before
        print("Time taken to {} {} bytes: {}".format(name, 100000 * 32, taken))
        print("{} bytes/second; {} bits/second".format(int((100000 * 32) / taken),
                                                       int((100000 * 32 * 8) / taken)))
    print("Number of private key operations per second: {}".format(10000 / taken))

if __name__ == "__main__":
    test_encrypt_decrypt()
