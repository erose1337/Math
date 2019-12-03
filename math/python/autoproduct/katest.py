from autoproduct import *

def test():
    A, B = generate_key(), generate_key()
    g = generate_vector()
    assert F(Ia, g) * a == F(A, g)
    assert F(Ib, g) * b == F(B, g)
    assert F(Ix, g) * x == F(X, g)
    assert F(Iy, g) * y == F(Y, g)


    assert F(X, g) * a == F(scale_matrix(X, a), g)
    assert F(A, g) * x == F(scale_matrix(A, x), g)

    assert F(X, g) * a == F(A, g) * x

    print("really?")

    pub1 = (F(A, g), F(B, g))
    pub2 = (F(X, g), F(Y, g))



    share1 = (a * pub2[0]) + (b * pub2[1])
    share2 = (x * pub1[0]) + (y * pub1[1])
    assert share1 == share2, (Ia, Ib, Ix, Iy)


if __name__ == "__main__":
    test()
