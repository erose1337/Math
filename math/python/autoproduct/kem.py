import modulargcd
import autoproduct
import utilities

G = [utilities.random_integer(modulargcd.PARAMETERS["m_size"]) >> 1 for
     element in range(autoproduct.PARAMETERS['n'])]

def generate_private_key(parameters=modulargcd.PARAMETERS,
                         keygenf=modulargcd.generate_key):
    return keygenf(parameters)

def generate_public_key(private_key, parameters=modulargcd.PARAMETERS,
                        encrypt=modulargcd.encrypt, G=G):
    return [encrypt(point, private_key, parameters) for point in G]

def generate_keypair(parameters=modulargcd.PARAMETERS,
                     keygenf=modulargcd.generate_key,
                     encrypt=modulargcd.encrypt, G=G):
    private_key = generate_private_key(parameters, keygenf)
    public_key = generate_public_key(private_key, parameters, encrypt, G)
    return public_key, private_key

def encapsulate(public_key, parameters=modulargcd.PARAMETERS, G=G):
    p = parameters['p']
    R = autoproduct.generate_key()                    # possibly should be / 2 instead of - 4?
    S = [utilities.random_integer(parameters["m_size"] - 4) for count in range(len(public_key))]

    # autoproduct only, no scaling; n! >= p
    #secret = autoproduct.F(R, g)
    #encapsulated = autoproduct(R, public_key)

    # single random scalar          n! >= p - log2(scalar)
    #secret = (s * autoproduct.F(R, G)) % p
    #encapsulated = (s * autoproduct.F(R, public_key)) % p

    # one scalar per element of the vector
    # injects the most amount of random data among these schemes and can use smaller dimension
    # n! >= p - n(log2(scalar))
    secret = autoproduct.F(R, [(G[i] * S[i]) % p for i in range(len(S))])
    encapsulated = autoproduct.F(R, [(public_key[i] * S[i]) % p for i in range(len(S))])
    return encapsulated, secret

def unencapsulate(encapsulated, private_key, parameters=modulargcd.PARAMETERS,
                  decrypt=modulargcd.decrypt):
    return decrypt(encapsulated, private_key, depth=2, parameters=parameters)

def test_kem():
    for count in range(1000):
        public_key, private_key = generate_keypair()
        challenge, solution = encapsulate(public_key)
        solution2 = unencapsulate(challenge, private_key)
        assert solution2 == solution, count

    from timeit import default_timer as timer
    from math import log
    iterations = 10000

    before = timer()
    for count in range(iterations):
        c, s = encapsulate(public_key)
    after = timer()
    taken = after - before
    print("Time taken to encapsulate {} {}-bit keys: {}".format(iterations, int(log(s, 2)), taken))

    before = timer()
    for count in range(iterations):
        s = unencapsulate(c, private_key)
    after = timer()
    taken = after - before
    print("Time taken to unencapsulate {} {}-bit keys: {}".format(iterations, int(log(s, 2)), taken))

    #with open("G.txt", "wb") as _file:
    #    _file.write(',\n'.join(str(item) for item in G))
    #    _file.flush()
    #with open("publickey.txt", "wb") as _file:
    #    _file.write(',\n'.join(str(item) for item in public_key))
    #    _file.flush()
    #with open("privatekey.txt", "wb") as _file:
    #    _file.write(",\n".join(str(private_key)))
    #    _file.flush()
    #with open("ciphertext.txt", "wb") as _file:
    #    _file.write(str(c))
    #    _file.flush()
    #with open("secret.txt", "wb") as _file:
    #    _file.write(str(s))
    #    _file.flush()

if __name__ == "__main__":
    test_kem()
