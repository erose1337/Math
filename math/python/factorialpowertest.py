from math import factorial, log
from fractions import gcd

def test_relation():
    p = 12
    q = 17
    n = p * q
    logn = log(n, 2)
    for k in range(p, q):
        kfactorial = factorial(k) % n
        assert gcd(kfactorial, n) == p, (n, gcd(kfactorial, n), p)
        generators = []
        exponents = []
        for r in range(1, q):
            g = p * r
            for x in range(2, n):
                if pow(g, x, n) == kfactorial:
                    exponents.append(x)
                    generators.append(g)
                    break
        print k, generators, exponents
        raw_input()

if __name__ == "__main__":
    test_relation()
