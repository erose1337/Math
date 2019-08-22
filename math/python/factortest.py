from fractions import gcd
import itertools

from utilities import is_prime
from utilities import prime_generator as _prime_generator

PRIME_COUNT = 32
_GENERATOR = _prime_generator()
PRIMES = [next(_GENERATOR) for count in range(PRIME_COUNT)]

def prime_generator(start=0, primes=PRIMES, _generator=_GENERATOR):
    if start < len(primes):
        for prime in primes[start:]:
            yield prime
        for prime in _generator:
            primes.append(prime)
            yield prime
    else:
        count = len(primes)
        while count < start:
            primes.append(next(_generator))
            count += 1
        yield primes[-1]
        for prime in _generator:
            primes.append(prime)
            yield prime

def factor(n, prime_count=32, gmax=2 ** 18):
    factorization = dict()
    if is_prime(n):
        factorization[n] = 1
        return factorization

    # guess some prime factors of the totient
    primes = []
    generator = prime_generator()
    next(generator) # skip 2
    factormax = 1
    for count in range(prime_count):
        primes.append(next(generator))
        factormax *= primes[-1]
    #if factormax > n:
    #    raise ValueError("factor_test too large; use less primes")
    gmin = 2
    while not factorization:
        selectors = itertools.product(*([1, 0] for count in range(prime_count)))
        next(selectors) # discard all 0s
        for factor_selection in selectors:
            factor_test = 4
            for index, selector_bit in enumerate(factor_selection):
                if selector_bit == 1:
                    factor_test *= primes[index]
            if factor_test > n:
                continue
            #print("testing {}".format(factor_test))
            for g in xrange(gmin, min(factor_test, gmax)):
                k = pow(g, factor_test, n)
                if k in (1, n - 1):
                    if k == n - 1:
                        print("-1")
                    continue
                if (k - 1) != 1:
                    _gcd = gcd(k, n)
                    if _gcd != 1: # only handles n = pq
                        #print("gcd({}^{} mod {}, {}) > 1".format(g, factor_test, n, n))
                        factorization[_gcd] = 1
                        factorization[n / _gcd] = 1
                        _primes = [prime for (i, prime) in enumerate(primes) if factor_selection[i]]
                        print("Success with g:{} b: {} x={}".format(g, ''.join((str(item) for item in factor_selection)), factor_test))
                        return factorization
                    _gcd = gcd(k - 1, n)
                    if _gcd != 1:
                        factorization[_gcd] = 1
                        factorization[n / _gcd] = 1
                        _primes = [prime for (i, prime) in enumerate(primes) if factor_selection[i]]
                        print("Success with g:{} b: {} x={}".format(g, ''.join((str(item) for item in factor_selection)), factor_test))
                        return factorization
        #print("Exhausted prime combinations, increasing gmax")
        #raw_input()
        gmin = gmax
        gmax **= 2

def test_factor(size=1, count=256, prime_count=8, gmax=2**16):
    from utilities import big_prime, factor_integer
    for _ in range(count):
        p = big_prime(size)
        q = big_prime(size)
        print("p - 1 factors: {}".format(factor_integer(p - 1)))
        print("q - 1 factors: {}".format(factor_integer(q - 1)))
        n = p * q
        print("Factoring {}".format(n))
        factorization = factor(n, prime_count, gmax)
        #mult = 2
        #while factorization is None:
        #    print("Factor base too small, increasing...")
        #    factorization = factor(n, prime_count, gmax ** mult)
        #    mult *= 2
        #if factorization is None:
        #    print factor_integer((p - 1) * (q - 1))
        #    raise ValueError("Failed to factor {}".format(n))
        assert set(factorization.keys()) == set((p, q)), (factorization, p, q)

if __name__ == "__main__":
    test_factor(3, 256, 10, 2 ** 2)
