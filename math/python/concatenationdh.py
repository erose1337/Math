from math import log, floor

from utilities import random_integer, big_prime

SECURITY_LEVEL = 32

def generate_parameters(security_level=SECURITY_LEVEL):
    G = 2
    width = 8
    w = G ** width
    p = big_prime(security_level)
#    lengths = [pow(w, i,
    parameters = {'w' : w, 'G' : G, 'p' : p, "width" : width}
    return parameters

PARAMETERS = generate_parameters(SECURITY_LEVEL)

#def concatenate(X, Y, w=parameters['w'], p=parameters['p']):
def add(X, Y, x_length, w=PARAMETERS['w'], p=PARAMETERS['p']):
    #print("Computing pow({} {})".format(w, x_length))
    return (X ^ (pow(w, x_length) * Y))# % p

def double(X, x_length, w=PARAMETERS['w'], p=PARAMETERS['p']):
    return add(X, X, x_length, w)

def scalar_mult(X, y, w=PARAMETERS['w'], p=PARAMETERS['p']):
    if 0 in (X, y):
        return 0
    output = 0
    output_length = 0
    X_length = 1
    while y:
        if y & 1:
            output = add(output, X, output_length, w, p)
            ##output ^= (w**output_length) * X # with g=2 could use shift instead
            output_length += X_length
        X = double(X, X_length, w, p)
        X_length *= 2
        y >>= 1
    #assert output == output % p
    return output

def test_arithmetic(parameters=PARAMETERS):
    X = 1
    Y = 2
    XY = add(X, Y, 1)
    assert XY == 513, format(XY, 'b').zfill(parameters["width"] * 2)

    X4 = double(XY, 2)
    assert X4 == (513 << 16) + 513, format(X4, 'b')

    X = 1
    k = 64
    kX = scalar_mult(X, k)
    bits = ''.join(item for item in [format(X, 'b').zfill(8)] * k)
    assert kX == int(bits, 2), format(kX, 'b')
    #assert kX == int(bits, 2) % parameters['p'], format(kX, 'b')

    G = 113 # any symbol in 0-255
    x = random_integer(4)
    y = random_integer(4)
    xG = scalar_mult(G, x)
    yG = scalar_mult(G, y)
    share_x = scalar_mult(yG, x)
    share_y = scalar_mult(xG, y)
    assert share_x == share_y, (share_x, share_y)

if __name__ == "__main__":
    test_arithmetic()
