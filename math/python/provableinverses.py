# RSA keygen refresher:
# p, q
# n = p * a
# t = (p - 1) * (q - 1)
#   = (p * q) - p - q + 1
#   = n - p - q  + 1
#   = n - k
# e = inverse(d, t)
#   = inverse(d, n - k)      id. 1

# Scheme keygen:
# p
# secret k
# e = inverse(d, p - k)      using id. 1
# e * d mod p - k == 1
#    - Given `e, p` the ability to find `d` implies the ability to recover the private exponent `d` in RSA
#       - assuming similar parameter sizes e.g. size of k, d
#       - choose `d` as small as possible while remaining secure (small d attacks on RSA as a guideline)

# noisy arithmetic:
#
#    x mod p - k = x + (x/p * k) mod p      P     k    d    x/p   k + x/p   d + k + x/p
#                                         # 64    32   32    32     96        96
#                                         # 96    48   48    32     80        128
#                                         # 128   64   64    32     96        160
#
#    x mod p - k = x + r mod p
#
# Keep the noise term r small and arithmetic mod p is equivalent to arithmetic mod p - k in the most significant bits
#
# have to make k smaller than in RSA
#   -


# ... sidetrack back to RSA:
#   compute d' = modular_inverse(e, n)
#   log2((e * d') % t) is half the size of log2(n)
#
# m^e^d' = m^e(d + r) = m^ed + er = m^(1 + er)        1 + er << t
#
