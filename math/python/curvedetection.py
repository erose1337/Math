CURVE_THRESHOLD = 2

def differences(samples):
    return [samples[i + 1] - samples[i] for i in range(len(samples) - 1)]

def average(samples):
    return sum(samples) / len(samples)

def find_curves(samples, threshold=CURVE_THRESHOLD):
    #print samples
    d1 = differences(samples) + [0]
    #print d1
    d2 = differences(d1) + [0]
    #print d2
    temp = [(sample if sample >= threshold else 0) for sample in d2]
    output = temp#[average(temp[i:i + 3]) for i in range(len(temp) - 2)]
    return [(samples[i] if x else 0) for i, x in enumerate(output)]

def test_find_curves():
    from math import ceil
    #samples = [1, 2, 10, 11, 12, 13]
    #samples = [1] * 256
    #for x in range(2, 256):
    #    samples[::x] = [(a + b) for a, b, in zip(samples[::x], [x] * int(ceil(256.0 / x)))]
    #samples = range(16) + [pow(x, 2) for x in range(16, 32)] + range(32, 48) + range(48, 256)
    #samples = [pow(x, 2) for x in range(16)] + range(16, 32) + [pow(x, 2) for x in range(32, 48)]
    #samples = range(4) + [pow(x, 2) for x in range(4, 8)] + range(8, 12) #+ [pow(x, 2) + 20 for x in range(12, 16)]
    samples = [pow(x, 2) + (10 * x) for x in range(128)] + [pow(x, 2) for x in range(128, 256)]
    #from os import urandom; samples = [ord(urandom(1)) for count in range(256)]
    curve_points = find_curves(samples)
    #print curve_points
    #print(len(samples), len(curve_points))

    with open("line.txt", "wb") as _file:
        for i, sample in enumerate(samples):
            _file.write("{} {}\n".format(i, sample))
        _file.flush()

    with open("curvetest.txt", "wb") as _file:
        for i, sample in enumerate(curve_points):
            if sample:
                _file.write("{} {}\n".format(i, sample))
        _file.flush()

    #with open("curvetest2.txt", "wb") as _file:
    #    for i, sample in enumerate(differences(curve_points)):
    #        _file.write("{} {}\n".format(i, sample))
    #    _file.flush()

def test_and_gnuplot():
    test_find_curves()
    import os
    os.system("gnuplot")

if __name__ == "__main__":
    #test_find_curves()
    test_and_gnuplot()
