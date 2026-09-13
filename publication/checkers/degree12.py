#!/usr/bin/env python3
"""Standalone GF64 certificate used in the short note; standard library only."""
MODULUS=0b1000011

def reduce_poly(a,b=MODULUS):
    while a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
    return a

def mul(a,b):
    out=0
    for i in range(b.bit_length()):
        if (b>>i)&1:out^=a<<i
    return reduce_poly(out)

def power(a,n):
    out=1
    for _ in range(n):out=mul(out,a)
    return out

def trace(a):
    out=0
    for _ in range(6):out^=a;a=mul(a,a)
    return out

def main():
    # A degree-six polynomial is irreducible iff it has no factor of degree<=3.
    assert all(reduce_poly(MODULUS,b)!=0 for d in (1,2,3) for b in range(1<<d,1<<(d+1)))
    x=2;y=20
    a=power(x,3)^x^1;b=mul(x,x)^x;c=power(x,5)^mul(x,x)^1
    assert mul(y,y)^mul(a,y)==b and c!=0
    assert power(x,64)==x and all(power(x,2**d)!=x for d in (1,2,3))
    inverse=power(mul(c,c),62)
    vector=[trace(mul(mul(b,h),inverse)) for h in (1,x,mul(x,x),y,mul(y,y))]
    assert vector==[0,0,1,1,0]
    radicand=mul(mul(b,mul(x,x)),inverse)
    values=[]
    for _ in range(6):values.append(radicand);radicand=mul(radicand,radicand)
    assert values==[48,60,47,38,36,32]
    print('DEGREE12_NOTE_CHECK=PASS; nonzero Frobenius gives16 degree12 places')
if __name__=='__main__':main()
