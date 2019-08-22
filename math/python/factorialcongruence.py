from math import factorial, sqrt, ceil
from fractions import gcd

def combine(values):
    for index in range(len(values)):
        output = values[index]
        #debug = [output]
        for value in values[index + 1:]:
            output *= value
        #    debug.append(value)
        #print("Combined: {}".format(debug))
        yield output

def test_relation():
    q = 5
    for p in (7, 11, 13, 17, 19):
        n = p * q
        values = [factorial(x) % n for x in range(1, p - 1)]
        print [(item % n) % q == 0 for item in values]
        for index in range(len(values)):
            if (values[index] % n) % q == 0:
                print index, p, q, n
                break

        for value in combine(values):
            assert (value % n) % q == 0, (value, n, p)
            assert gcd(n, value % n) == q

if __name__ == "__main__":
    test_relation()
