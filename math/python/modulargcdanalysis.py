import itertools

from utilities import random_integer, is_prime

def examine_distribution(p, limit):
    outputs = []
    for x in range(p):
        outputs.extend((x * r) % p for r in range(1, limit + 1))
    return [outputs.count(value) for value in range(p)]

def analyze(p, limit, x_size):
    assert pow(limit, 2) + 1 == p
    outputs = []
    for x in range(p):
        samples = [(x * r) % p for r in range(1, limit + 1)]
        outputs.append(samples)

    x = random_integer(x_size) % p # pick a key
    while not x:
        x = random_integer(x_size) % p # pick a key
    samples = [(x * r) % p for r in range(1, (limit / 2) + 1)]
    candidates = []
    print x, samples
    for sample in samples:
        for _x, row in enumerate(outputs):
            if sample in row:
                candidates.append(row)
            else:
                try:
                    candidates.remove(row)
                except ValueError:
                    continue
    print p, len(candidates), candidates

def test1():
    for p in range(5, 102):
    #for r in range(2, 100):
        #p = (r ** 2) + 1
        samples = examine_distribution(p, p - 1)
        variation = len(set(samples))
        print variation
        if variation == 1:
            assert is_prime(p), p
        if is_prime(p):
            assert variation == 1
        #    raw_input()
        #else:
        #    assert not is_prime(p), p
    # appears that you could convert this into a primality test
    # given some n, set r = sqrt(n - 1)
    # if r is not an integer, output False
    # else:
    #      for 0 < x < p:
    #          samples.extend([xy mod p for 0 < y <= r])
    # to prove n is prime, demonstrate that each k appears in `samples` exactly r times
    #   - cost: exponential in size of n
    # to prove n is composite, find some value k < p that appears in `samples` more or less than r times
    #   - cost: ?
    #       - can test different k in parallel
    #       - can test same k in parallel?
    #           - each of t workers looks at ...?
    #       - xy mod p = x for y = 1 could be used to prune search space

def test_sample_frequency():
    p = 257
    outputs = []
    for x in range(1, p):
        outputs.append([(x * r) % p for r in range(1, 17)])

    _hits = []
    sample_count = 1
    for values in itertools.product(*(range(1, p) for count in range(sample_count))):
        hits = 0
        for row in outputs:
            for value in values:
                if value not in row:
                    break
            else:
                hits += 1
        _hits.append(hits)

    from string import lowercase as _symbols
    for item in sorted(set(_hits)):
        print("The number of times {} appeared in {} rows: {}".format(tuple(_symbols[-sample_count:]), item, _hits.count(item)))

    # The number of times s appeared in 16 rows: 256

    # The number of times (s_1, s_2) appeared in 0 rows: 24832
    # The number of times (s_1, s_2) appeared in 1 rows: 29696
    # The number of times (s_1, s_2) appeared in 2 rows: 6144
    # The number of times (s_1, s_2) appeared in 3 rows: 2048
    # The number of times (s_1, s_2) appeared in 4 rows: 1024
    # The number of times (s_1, s_2) appeared in 5 rows: 1024
    # The number of times (s_1, s_2) appeared in 8 rows: 512
    # The number of times (s_1, s_2) appeared in 16 rows: 256

    # The number of times (s_1, s_2, s_3) appeared in 0 rows: 15898368
    # The number of times (s_1, s_2, s_3) appeared in 1 rows: 766464
    # The number of times (s_1, s_2, s_3) appeared in 2 rows: 82944
    # The number of times (s_1, s_2, s_3) appeared in 3 rows: 15360
    # The number of times (s_1, s_2, s_3) appeared in 4 rows: 7680
    # The number of times (s_1, s_2, s_3) appeared in 5 rows: 4608
    # The number of times (s_1, s_2, s_3) appeared in 8 rows: 1536
    # The number of times (s_1, s_2, s_3) appeared in 16 rows: 256


if __name__ == "__main__":
    #test1()
    #analyze(101, 10, 32)
    test_sample_frequency()
