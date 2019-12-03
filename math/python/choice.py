import operator
from utilities import random_integer
def choice(a, b, c): return c ^ (a & (b ^ c))
def noise_term(word_size): return reduce(operator.and_, (random_integer(word_size) for count in range(2)))
def f(A, B, C, noise_size=8): return sum(choice(A[i], B[i], C[i]) + noise_term(word_size) for i in range(len(A)))

def test_choice():
    size = 8
    for _ in range(1024):
        a, b, c = [random_integer(size) for _ in range(3)]
        r, s = [noise_term(size) for _ in range(2)]
        out1i = choice(a, b, c) + r
        out2i = choice(a, c, b) + s
        assert out1i + out2i == b + c + r + s

        out1b = choice(a, b, c) ^ r
        out2b = choice(a, c, b) ^ s
        assert out1b ^ out2b == b ^ c ^ r ^ s

def test_f():
    size = 8; N = 2
    for _ in range(1024):
        a, b, c = [[random_integer(size) for _ in range(N)] for _ in range(3)]
        output = f(a, b, c)

if __name__ == "__main__":
    test_choice()
