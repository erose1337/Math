def xorsum(*args):
    output = 0
    for item in args:
        output ^= item
    return output

def dotproduct(v1, v2):
    return sum(v1[i] * v2i for i, v2i in enumerate(v2))

def dotproduct2(v1, v2):
    return xorsum(*(v1[i] & v2[i] for i in range(len(v1))))

def mmul(m, v, dot=dotproduct):
    try:
        return [dot(row, v) for row in m]
    except (OverflowError, TypeError):
        return [[dot(row, _v) for row in m] for _v in v]

def scale_tensor(t, s):
    return [scale_matrix(m, s) for m in t]

def scale_matrix(m, s):
    return [scale_vector(row, s) for row in m]

def scale_vector(v, s):
    return [x * s for x in v]

def add_tensor(t1, t2):
    return [add_matrix(t1[i], t2[i]) for i in range(len(t1))]

def add_matrix(m1, m2):
    return [add_vector(m1[i], m2[i]) for i in range(len(m1))]

def add_vector(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]

def xor_vector(v1, v2):
    return [v1[i] ^ v2[i] for i in range(len(v1))]

def entrywise_productm(m1, m2):
    return [entrywise_productv(m1[i], m2[i]) for i in range(len(m1))]

def entrywise_productv(v1, v2):
    return [v1[i] * v2[i] for i in range(len(v1))]
