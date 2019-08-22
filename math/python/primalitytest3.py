from utilities import isqrt

def is_square(n):
    return pow(isqrt(n), 2) == n

def is_prime(n):
    if n in (2, 3):
        return True
    if ((n ** 2) - 1) % 24 == 0:
        return True
    return False

def test_is_prime():
    from utilities import is_prime as millerrabin
    outputs = []
    for n in range(3, 1000000):
        outputs.append(is_prime(n) == millerrabin(n))
    outputstr = str(outputs)
    matches = outputstr.count("True")
    nonmatches = outputstr.count("False")
    print("{} matches; {} non-matches; {} total tests".format(matches, nonmatches, len(outputs)))
    print("Accuracy: {}%".format(matches / float(len(outputs))))

if __name__ == "__main__":
    test_is_prime()
