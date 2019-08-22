from math import log

from utilities import prime_generator, random_integer, factor_integer, is_prime

_gen = prime_generator()
PRIMES = [next(_gen) for x in range(200)]
del _gen

def find_generator(n, factors):
    while True:
        candidate = random_integer(int(log(n, 2)) * 8) % n # biased, but probably fine
        for prime in factors:
            b = pow(candidate, n / prime, n + 1)
            if b == 1:
                break
        else:
            #outputs = []
            #for x in range(n):
            #    gx = pow(candidate, x, n + 1)
            #    print("Testing if g^{} in outputs already".format(x))
            #    if gx in outputs:
            #        print len(set(outputs)), outputs, gx, n
            #        raise ValueError("Did not find correct generator")
            #    outputs.append(gx)
            #print("Found generator for {}".format(n))
            return candidate

def find_order(a, n, factorization):
    t = n
    print("Finding order")
    for prime, exponent in factorization.items():
        t = t / (prime ** exponent)
        print "t: ", t
        a1 = pow(a, t, n + 1)
        while a1 != 1:
            #print a1, t
            a1 = pow(a1, prime, n + 1)
            t *= prime
    return t

def primality_test(n):
    # assume n is prime. The totient is n - 1
    if n in (2, 3):
        return True
    totient = n - 1
    #print("Factoring {}".format(totient))
    factorization = factor_integer(totient)
    factors = factorization.keys()
    generator = find_generator(totient, factors)
    #generator = find_generator(n, {n: 1})
    if generator == 0:
        return False
    print("Generator: {}".format(generator))
    #print totient % generator == 0, (totient % generator)
    #while True:
    #    generator = find_generator(totient, factors)
    #    outputs = []
    #    for x in range(n - 1):
    #        gx = pow(generator, x, n)
    #        if gx in outputs:
    #    #        print("Did not find a proper generator {}/{}".format(x, n))
    #            break
    #        else:
    #            outputs.append(gx)
    #    else:
    #    #    print("Found a proper generator")
    #        break
    #order = find_order(generator, n, factorization)
    #print("Order of {}^x mod {}: {}".format(generator, n, order))
    exponent = ((pow(totient, 2) + totient) / 2) % totient
    if pow(generator, exponent, n) == n - 1:
        return True
    else:
        return False

def test_primality_test(test_count, number_size):
    from utilities import big_prime, random_integer, is_prime
    for count in range(test_count):
        p = big_prime(number_size)
        result = primality_test(p)
        #assert result == primality_test(p)
        assert result == True, (p, result, primality_test(p), is_prime(p))

if __name__ == "__main__":
    test_primality_test(256, 1)
