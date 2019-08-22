def primality_test(n, gmax=1024):
#    if n in (2, 3): # would remove the max statement from the range call below
#        return True
    exponent = ((pow(n - 1, 2) + (n - 1)) / 2) % (n - 1)
    for g in range(min(max(3, n - 1), gmax)):
        if pow(g, exponent, n) == n - 1:
            return True
    else:
        return False

def test_primality_test():
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26]
    for prime in primes:
        assert primality_test(prime) == True, prime
    for composite in composites:
        assert primality_test(composite) == False, composite

if __name__ == "__main__":
    test_primality_test()
