import operator

def evaluate(x, polynomial, coefficients):
    return sum(coefficients[i] * pow(x, polynomial[i]) for i in range(len(polynomial)))

def recover_polynomial(x, y):
    polynomial = []
    coefficients = []
    while True:
        t = y - evaluate(x, polynomial, coefficients)
        if t == 0:
            break
        power = 0
        while int(abs(t)) >= int(abs(x)):
            if t < 0: # e.g. -303 / 100 outputs -4, but it needs to output -3
                t = (t + (x - (t % x))) / x
            else:
                t /= x
            power += 1
        polynomial.append(power)
        coefficients.append(t)
    return list(reversed(polynomial)), list(reversed(coefficients))

def format_polynomial(polynomial, coefficients):
    _string = ("{}x^{} + " * len(polynomial))[:-3]
    return _string.format(*reduce(operator.add, zip(coefficients, polynomial)))

def test_recover_polynomial():
    polynomial = [1, 3, 4, 6, 8, 10]
    coefficients = [1, 2, 3, 5, 7, 9]
    x = 11
    y = evaluate(x, polynomial, coefficients)
    _polynomial, _coefficients = recover_polynomial(x, y)
    assert evaluate(x, _polynomial, _coefficients) == y
    assert polynomial == _polynomial, (polynomial, _polynomial)
    assert coefficients == _coefficients, (coefficients, _coefficients)
    x2 = 107
    y2 = evaluate(x2, polynomial, coefficients)
    _polynomial2, _coefficients2 = recover_polynomial(x2, y2)
    assert evaluate(x2, _polynomial2, _coefficients2) == y2
    y_test = evaluate(x, _polynomial2, _coefficients2)
    assert y == y_test, (y, y_test) # fails
    assert _polynomial == _polynomial2, (_polynomial, _polynomial2)
    assert _coefficients == _coefficients2, (_coefficients, _coefficients2)

    #print("Starting more unit tests")
    tests = [([0], [-8]),
             ([0, 1], [1, 2]),
             ([0, 1, 2], [-1, -2, -3]),
             ([0, 3, 4, 7], [-1, 2, -3, 4])]
    x = 10
    for polynomial, coefficients in tests:
        y = evaluate(x, polynomial, coefficients)
        print("Testing on f({}) -> {}".format(format_polynomial(polynomial, coefficients), y))
        _polynomial, _coefficients = recover_polynomial(x, y)
        string1 = format_polynomial(polynomial, coefficients)
        string2 = format_polynomial(_polynomial, _coefficients)
        print("True polynomial: {}".format(string1))
        print("Recovered polynomial: {}".format(string2))
        print
        assert evaluate(x, _polynomial, _coefficients) == y
        assert _polynomial == polynomial, (_polynomial, polynomial)
        assert _coefficients == coefficients, (_coefficients, coefficients)

if __name__ == "__main__":
    test_recover_polynomial()
