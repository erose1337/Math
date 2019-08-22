# es + r mod n
# 16384 3276    7372


#s(e + x) + r
#es + xs + r

from utilities import random_integer, modular_inverse, gcd

MODULUS_SIZE = 2048
BETA = .25
DELTA = .55
MODULUS_NOISE_SIZE = int(MODULUS_SIZE * BETA)
INVERSE_SIZE = int(MODULUS_SIZE * DELTA)
MODULUS = (2 ** (MODULUS_SIZE * 8)) << 1
PARAMETERS = {"modulus_size" : MODULUS_SIZE, "beta" : BETA, "delta" : DELTA,
              "modulus_noise_size" : MODULUS_NOISE_SIZE,
              "inverse_size" : INVERSE_SIZE, "modulus" : MODULUS,
              "s_size": MODULUS_SIZE - INVERSE_SIZE - MODULUS_NOISE_SIZE,
              "r_size" : MODULUS_SIZE - INVERSE_SIZE}

def generate_private_key(parameters=PARAMETERS):
    inverse_size = parameters["inverse_size"]
    modulus = parameters["modulus"]
    k = random_integer(parameters["modulus_noise_size"])
    d = random_integer(inverse_size)
    while gcd(d, modulus + k) != 1:
        k = random_integer(parameters["modulus_noise_size"])
    return d, k

def generate_public_key(private_key, parameters=PARAMETERS):
    d, k = private_key
    return modular_inverse(d, parameters["modulus"] + k)

def generate_keypair(parameters=PARAMETERS):
    private_key = generate_private_key(parameters)
    public_key = generate_public_key(private_key, parameters)
    return public_key, private_key

def encapsulate_key(public_key, parameters=PARAMETERS):
    s = random_integer(parameters["s_size"])
    r = random_integer(parameters["r_size"])
    n = parameters["modulus"]
    return ((public_key * s) + r) % n, s

def recover_secret(ciphertext, private_key, parameters=PARAMETERS):
    d, k = private_key
    n = parameters["modulus"]
    return ((ciphertext * d) % (n + k)) % d

def unit_test():
    for x in range(10000):
        public_key, private_key = generate_keypair()
        ciphertext, secret = encapsulate_key(public_key)
        _secret = recover_secret(ciphertext, private_key)
        assert secret == _secret, x

if __name__ == "__main__":
    unit_test()
