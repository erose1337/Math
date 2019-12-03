#public key : K = a^2 + b^2
#private key: a, b
#sign:
#    X = x^2 + y^2
#    r = h(X | m)
#    R = r^2 + r^2
#    find c, d such that c^2 + d^2 = K * X * R
#     = (a^2 + b^2) * (x^2 * y^2) * (r^2 + r^2)         # expand terms
#     = ((ax - by)^2 + (ay + bx)^2) * (r^2 + r^2)       # brahmagupta-fibonacci identity
#     = (j^2 + k^2) * (r^2 + r^2)                       # rename terms
#     = (jr - kr)^2 + (jr + kr)^2                       # brahmagupta-fibonacci identity
#       (jr - kr), (jr + kr) = c, d                     # knowing a, b, x, y, r, allows computation of c, d
#    output X, c, d
#verify:
#    r = h(X, m)
#    R = r^2 + r^2
#    S = K * X * R
#    if c^2 + d^2 == S:
#        output True
#    else:
#        output False
import hashlib

from utilities import random_integer, bytes_to_integer, integer_to_bytes

SECURITY_LEVEL = 32

def _hash(hash_input, algorithm=hashlib.sha256):
    return bytes_to_integer(bytearray(algorithm(hash_input).digest()))

def generate_parameters(security_level=SECURITY_LEVEL):
    size = security_level
    return {"size" : size, "hash" : _hash}

PARAMETERS = generate_parameters(SECURITY_LEVEL)

def cat(integer1, integer2, parameters=PARAMETERS):
    size = parameters["size"]
    return integer_to_bytes(integer1, size) + integer_to_bytes(integer2, size)

def generate_private_key(parameters=PARAMETERS):
    size = parameters["size"]
    a, b = [random_integer(size) for count in range(2)]
    if (pow(a, 2) + pow(b, 2)) % 4 == 1:
        a, b, = generate_private_key(parameters)
    return a, b

def generate_public_key(private_key, parameters=PARAMETERS):
    a, b = private_key
    return pow(a, 2) + pow(b, 2)

def generate_keypair(parameters=PARAMETERS):
    private_key = generate_private_key(parameters)
    public_key = generate_public_key(private_key, parameters)
    return public_key, private_key

def sign(private_key, message, parameters=PARAMETERS):
    size = parameters["size"]; h = parameters["hash"]
    a, b = private_key
    x, y = generate_private_key(parameters)
    X = pow(x, 2) + pow(y, 2)
    r1 = h(cat(X, message))
    r2 = h(cat(message, X))
    R = pow(r1, 2) + pow(r2, 2)
    K = pow(a, 2) + pow(b, 2)

    t1 = (a * x) - (b * y)
    t2 = (a * y) + (b * x)
    assert pow(t1, 2) + pow(t2, 2) == K * X

    c = (t1 * r1) - (t2 * r2)
    d = (t1 * r2) + (t2 * r1)
    assert pow(c, 2) + pow(d, 2) == K * X * R
    return X, c, d

def verify(public_key, message, signature, parameters=PARAMETERS):
    X, c, d = signature
    h = parameters["hash"]
    r1 = h(cat(X, message))
    r2 = h(cat(message, X))
    R = pow(r1, 2) + pow(r2, 2)
    S = public_key * X * R
    if (S == 0) or (c == 0) or (d == 0):
        return False

    if pow(c, 2) + pow(d, 2) == S:
        return True
    else:
        return False

def test_sign_verify():
    for count in range(1000):
        public, private = generate_keypair()
        m = bytes_to_integer(bytearray("test message!"))
        signature = sign(private, m)
        assert verify(public, m, signature)

if __name__ == "__main__":
    test_sign_verify()
