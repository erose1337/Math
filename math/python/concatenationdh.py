from math import log, floor

from utilities import random_integer, big_prime

SECURITY_LEVEL = 32

def generate_parameters(security_level=SECURITY_LEVEL):
    G = 2
    width = 8
    w = G ** width
    p = big_prime(security_level)
    assert p % w
#    lengths = [pow(w, i,
    parameters = {'w' : w, 'G' : G, 'p' : p, "width" : width,
                  "security_level" : security_level}
    return parameters

PARAMETERS = generate_parameters(SECURITY_LEVEL)

def shift(X, shift_count, w=PARAMETERS['w'], p=PARAMETERS['p']):
    return X * pow(w, shift_count, p) # memoization not found to be helpful

#def concatenate(X, Y, w=parameters['w'], p=parameters['p']):
def add(X, Y, x_length, w=PARAMETERS['w'], p=PARAMETERS['p'], _memo=dict()):
    #return (X + shift(Y, x_length, w, p)) % p # memoizing saves some time, but is obviously more vulnerable
    try:
        return _memo[(X, Y, x_length, w, p)]
    except KeyError:
        output = _memo[(X, Y, x_length, w, p)] = (X + shift(Y, x_length, w, p)) % p
        return output

def double(X, x_length, w=PARAMETERS['w'], p=PARAMETERS['p']):
    return add(X, X, x_length, w) # memoization not found to be helpful

def scalar_mult(X, y, w=PARAMETERS['w'], p=PARAMETERS['p']):
    if 0 in (X, y):
        return 0
    output = 0
    output_length = 0
    X_length = 1
    while y:
    #    print y
        if y & 1:
            output = add(output, X, output_length, w, p)
            output_length += X_length
        X = double(X, X_length, w, p)
        X_length *= 2
        y >>= 1
    return output % p

def test_arithmetic(parameters=PARAMETERS):
    X = 1
    Y = 2
    XY = add(X, Y, 1)
    assert XY == 513 % parameters['p'], (format(XY, 'b').zfill(parameters["width"] * 2), format(513, 'b').zfill(parameters["width"] * 2))
    print("add/concatenation test passed")

    X4 = double(XY, 2)
    assert X4 == ((513 << 16) + 513) % parameters['p'], '\n'.join(('\n' + format(X4, 'b'), format(((513 << 16) + 513) % parameters['p'], 'b')))
    print("double test passed")

    X = 1
    k = 64
    kX = scalar_mult(X, k)
    bits = ''.join(item for item in [format(X, 'b').zfill(8)] * k)
    known_value = int(bits, 2) % parameters['p']
    #print format(kX ^ known_value, 'b')
    assert kX == known_value, '\n'.join(('\n' + format(kX, 'b'), format(known_value, 'b'), str(len(format(kX, 'b'))), str(len(format(known_value, 'b')))))
    assert kX == int(bits, 2) % parameters['p'], format(kX, 'b')

    G = parameters['G']
    #print("G: {}; P: {}".format(parameters['G'], parameters['p']))
    from timeit import default_timer as time_stamp
    before = time_stamp()
    agreements = 256
    for count in range(agreements):
        x = random_integer(parameters["security_level"])
        y = random_integer(parameters["security_level"])
        xG = scalar_mult(G, x)
        yG = scalar_mult(G, y)
        share_x = scalar_mult(yG, x)
        share_y = scalar_mult(xG, y)
        assert share_x == share_y
        #print("x: {}".format(x))
        #print("y: {}".format(y))
        #print("xG: {}".format(xG))
        #print("yG: {}".format(yG))
        #print("xyG: {}".format(share_x))
    after = time_stamp()
    print("scalar_mult test passed")
    print("Number of key agreements performed: {}".format(agreements))
    print("4 scalar_mult per key agreement = {} scalar_mults computed".format(agreements * 4))
    print("Time taken: {}".format(after - before))

if __name__ == "__main__":
    test_arithmetic()
