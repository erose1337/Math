import random
import copy
from os import urandom
import operator
print("Warning: miniapencrypt.py uses insecure `random` module and is not intended for serious use.")

P = 115792089237316195423570985008687907853269984665640564039457584007913129640233
N = 16; K = 6; S = 32
ID = [[0 for count in range(N)] for _ in range(N)]
for i in range(N):
    ID[i][i] = 1

def dotproduct(v1, v2): return sum(v1[i] * v2i for i, v2i in enumerate(v2))
def add_tensor(t1, t2): return [add_matrix(t1[i], t2[i]) for i in range(len(t1))]
def add_matrix(m1, m2): return [add_vector(m1[i], m2[i]) for i in range(len(m1))]
def add_vector(v1, v2): return [v1[i] + v2[i] for i in range(len(v1))]
def scale_tensor(t, s): return [scale_matrix(m, s) for m in t]
def scale_matrix(m, s): return [scale_vector(row, s) for row in m]
def scale_vector(v, s): return [x * s for x in v]
def mmul(m, v): return [dotproduct(row, v) for row in m]
def bytes_to_integer(data): output = 0; size = len(data); return reduce(operator.or_, (data[index] << (8 * size - 1 - index) for index in range(size)))
def random_integer(s): return bytes_to_integer(bytearray(urandom(s)))
def generate_permutation_matrix(n=N, id=ID): id = copy.deepcopy(id); random.shuffle(id); return id
def generate_permutation_tensor(n=N, k=K): return [generate_permutation_matrix(n) for count in range(k)]
def generate_key(n=N, s=S): return [random_integer(s) for count in range(n)]
def generate_seed(n=N, k=K): return generate_permutation_tensor(n, k)
def F(T, k): return dotproduct(k, reduce(add_vector, [mmul(M, k) for M in T]))
def encrypt(message, key, n=N, k=K, p=P): G = generate_seed(n, k); return G, (message + F(G, key)) % p
def decrypt(cryptogram, key, p=P): return (cryptogram[1] - F(cryptogram[0], key)) % p
def add_cryptogram(c1, c2): return (add_tensor(c1[0], c2[0]), c1[1] + c2[1])
def scale_cryptogram(c1, s, p=P): return scale_tensor(c1[0], s), (c1[1] * s) % p


def test_encrypt_decrypt():
    for count in range(1000):
        key = generate_key()
        c1 = encrypt(1, key)
        c2 = encrypt(2, key)
        c3 = add_cryptogram(c1, c2)
        assert decrypt(c1, key) == 1
        assert decrypt(c2, key) == 2
        assert decrypt(c3, key) == 3

        r1, r2 = [random_integer(S) % P for _ in range(2)]
        c1 = encrypt(r1, key); c2 = encrypt(r2, key); c3 = add_cryptogram(c1, c2)
        assert decrypt(c1, key) == r1
        assert decrypt(c2, key) == r2
        assert decrypt(c3, key) == (r1 + r2) % P

        scaledc1 = scale_cryptogram(encrypt(1, key), r1)
        assert decrypt(scaledc1, key) == r1

if __name__ == "__main__":
    #test_F()
    #test2()
    test_encrypt_decrypt()
