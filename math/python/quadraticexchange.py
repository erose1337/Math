#y(aww + bz) = awwy + byz       make b, y, z large?
#z(axx + by) = axxz + byz
#                k     L
#                L = k + security_level
#
#                w, x = 32
#                a, b = 32
#                y, z = 64
#            64 + (32 * 3), 32 + (64 * 2) = 64 + 96, 128 + 32
#
# (aww + bz)(axx + by) = aawwxx + abwwy + abxxz + bbyz
#                      / a
#                      = awwxx + bwwy + bxxz + bbyz/a
#                      / b
#                      = awwxx/b + wwy + xxz + byz/a

from utilities import random_integer

SECURITY_LEVEL = 32

def generate_parameters(security_level=SECURITY_LEVEL):
    parameters = {"security_level" : security_level, "constant_size" : security_level,
                  "square_size" : security_level, "key_size" : security_level * 2,
                  "constants" : (random_integer(security_level), random_integer(security_level * 2)),
                  "shift_count" : security_level * 5 * 8}
    return parameters

PARAMETERS = generate_parameters(SECURITY_LEVEL)

def generate_private_key(parameters=PARAMETERS):
    return random_integer(parameters["key_size"])

def generate_public_key(y, parameters=PARAMETERS):
    x = random_integer(parameters["square_size"])
    a, b = parameters["constants"]
    return (a * pow(x, 2)) + (b * y)

def generate_keypair(parameters=PARAMETERS):
    private_key = generate_private_key(parameters)
    public_key = generate_public_key(private_key, parameters)
    return public_key, private_key

def generate_shared_information(y, public_key, parameters=PARAMETERS):
    return (y * public_key) >> parameters["shift_count"]

def unit_test():
    pub1, priv1 = generate_keypair()
    pub2, priv2 = generate_keypair()
    share1 = generate_shared_information(priv1, pub2)
    share2 = generate_shared_information(priv2, pub1)
    #print format(share1, 'b')
    #print format(share2, 'b')
    print share1
    print share2

if __name__ == "__main__":
    unit_test()
