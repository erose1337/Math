from utilities import random_integer

def calculate_frequency(n, iterations=1024):
    attempts = []
    for iteration in range(iterations):
        #gen = iter(samples)
        for count in range(1024):
            r = random_integer(16)#next(gen)
            if r % n == 0:
                break
        attempts.append(count)
    average_until_found = sum(attempts) / len(attempts)
    absolute_error = n - average_until_found
    return absolute_error
    #if absolute_error:
    #return absolute_error / float(n)
    #else:
    #    return 0

def test_frequencies():
    accuracy = []
    for n in range(2, 256):
        print n
        #print("{}: {}".format(n, calculate_frequency(n)))
        accuracy.append(calculate_frequency(n))
    print sum(accuracy) / len(accuracy)

if __name__ == "__main__":
    test_frequencies()
