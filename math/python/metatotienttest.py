from utilities import random_integer, factor_integer

def totient(*prime_factors):
    output = 1
    for prime in prime_factors:
        output *= prime - 1
    return output

def test():
    x = random_integer(2)
    while True:
        print("Factoring x...")
        factors = factor_integer(x)
        if all(exponent == 1 for exponent in factors.values()):
            t = totient(*factors.keys())
            print("Factoring totient...")
            factors_of_totient = factor_integer(t)
            if all(exponent == 1 for exponent in factors.values()):
                metatotient = totient(*factors_of_totient.keys())
                break
    print("x: {}".format(x))
    print("t: {}".format(t))
    print("metatotient: {}".format(metatotient))

    # scalars use x as the modulus
    # exponents uses totient as the modulues
    # do hyper-exponents use metatotient as the modulus?
    #   if the pattern applies in general, then there is a limit to the number of hyper operations
    #       since totient(k) < k, totient(totient(...totient(k))) must eventually shrink completely

    #       def f_0(x):
    #           return x + 1
    #
    #       def f_1(x, y):
    #           for i in range(1, y + 1):
    #               f_0(x)
    #       def f_2(x, y):
    #           for i in range(1, y + 1) :
    #               x = f_1(x, x)
    #       def f_3(x, y):
    #           for i in range(1, y + 1):
    #               x = f_2(x, x)
    #


if __name__ == "__main__":
    test()
