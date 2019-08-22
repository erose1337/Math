from utilities import random_integer, modular_inverse

def choke_egcd():
    n = 2 ** 16384
    k = random_integer(4096)
    d = random_integer(int(16384 * .55) / 8)
    modular_inverse(d, n + k)

if __name__ == "__main__":
    choke_egcd()
