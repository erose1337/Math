import random

p = 2 ** 255 - 66601
o = 2 * p + 3
c = (o - 1) / 16
A0 = [1, 0]


#t = ax - by
#u = ay + bx

def VADD(a,b):
    cosab = (a[0]*b[0] - a[1]*b[1]) % p
    sinab = (a[0]*b[1] + a[1]*b[0]) % p
    return [cosab, sinab]

def VMUL(z,n):
    OUT = A0
    PO2 = z
    while n>0:
        if n%2 == 1:
            OUT = VADD(OUT, PO2)
        PO2 = VADD(PO2, PO2)
        n //= 2
    return OUT

G = [8453775511928033057375054296276238971717940179762476598864302663859193602897, 29693326938214728262044596114061638353154103835233260595144813889643304809403]

print "-- x --"
x = random.randint(1, c)
print "x="+str(x)
X = VMUL(G, x)
print "X="+str(X)

print "-- y --"
y = random.randint(1, c)
print "y="+str(y)
Y = VMUL(G, y)
print "Y="+str(Y)

print "-- * --"
YX = VMUL(Y, x)
print "YX="+str(YX)
XY = VMUL(X, y)
print "XY="+str(XY)

assert XY == YX
