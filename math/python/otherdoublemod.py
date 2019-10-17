#   x(yr + m) mod P == xyr + xm mod P
# yr < P    m < y          ^ set m = 0; given xyr mod P, output x, y;
# m = y = r = 32             re-write xyr as kr mod P; given kr mod P, output k
# P = x = 64

# x(yr + n) * x(ys + m)
# xa * xb
# xxab
# xx(yr + n)(ys + m)
# xx(yyrs + yrm + ysn + mn)
# xx(
#    yyrs + yrm + ysn + mn
#   )

from utilities import random_integer, is_prime, modular_inverse

SECURITY_LEVEL = 32

def generate_parameters(security_level=SECURITY_LEVEL):
    parameters = {"y_size" : security_level, "m_size" : security_level,
                  "r_size" : security_level, "p_size" : security_level * 2,
                  "x_size" : security_level * 2}
    return parameters

PARAMETERS = generate_parameters()

def find_closest_prime(n):
    offset = 1
    while not is_prime(n + offset):
        offset += 2
    return offset

def generate_p(parameters=PARAMETERS):
    p_size = parameters["p_size"]
    p_start = 2 ** ((p_size * 8) + 1) # * 8 converts to bits
    offset = find_closest_prime(p_start)
    return p_start + offset

PARAMETERS['p'] = generate_p(PARAMETERS)

def generate_key(parameters=PARAMETERS):
    x_size, y_size = parameters["x_size"], parameters["y_size"]
    p = parameters['p']
    x = random_integer(x_size)
    y = random_integer(y_size) | (1 << ((y_size * 8) - 1))
    return x, y, modular_inverse(x, p)

def encrypt(m, key, parameters=PARAMETERS):
    r = random_integer(parameters["r_size"])
    x, y, d = key
    p = parameters['p']
    assert m < y
    t = (y * r) + m
    assert t < p
    t = (x * t)
    assert t > p
    return t % p

def decrypt(c, key, parameters=PARAMETERS):
    x, y, d = key
    p = parameters['p']
    return ((d * c) % p) % y

def test_encrypt_decrypt():
    key = generate_key()
    for count in range(100):
        m = 0
        c = encrypt(m, key)
        m2 = decrypt(c, key)
        assert m2 == m, (m2, m)

        c2 = encrypt(m, key)

        #print c
        #print c2

        m3 = decrypt(c + c2, key)
        assert m3 == 0, m3
        assert decrypt(encrypt(2, key) + encrypt(2, key), key) == 4

        m = random_integer(32) >> 2
        m2 = random_integer(32) >> 2
        assert decrypt(encrypt(m, key) + encrypt(m2, key), key) == (m + m2) % PARAMETERS['p']

    from timeit import default_timer as timer
    for name, function in [("encrypt", encrypt), ("decrypt", decrypt)]:
        before = timer()
        for count in range(100000):
            function(0, key)
        after = timer()
        taken = after - before
        print("Time taken to {} {} bytes: {}".format(name, 10000 * 32, taken))
        print("{} bytes/second; {} bits/second".format(int((10000 * 32) / taken),
                                                       int((10000 * 32 * 8) / taken)))


if __name__ == "__main__":
    test_encrypt_decrypt()
