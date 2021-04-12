import numpy as np

def pad(P, n):
    """
    Pads the polynomial P with 0s to extend its length to n
    """
    res = np.zeros(n)
    res[:len(P)] = P
    return res

def shift(P, n):
    """
    Multiplies the polynomial P by x^n
    """
    res = np.zeros(len(P) + n)
    res[n:] = P
    return res

def multiply(P, Q):
    assert(len(P) == len(Q))
    n = len(P)

    if n == 1:
        return P * Q    # element-wise product

    assert(n % 2 == 0)

    A = P[n//2:]
    B = P[:n//2]
    C = Q[n//2:]
    D = Q[:n//2]

    AC = multiply(A, C)
    BD = multiply(B, D)
    ADBC = AC + BD - multiply(C-D, A-B)
    ret = pad(BD, n + len(BD)) + shift(pad(ADBC, len(ADBC) + n // 2), n//2) + shift(AC, 2 * n -1 -len(AC))
    for i in range(len(ret)-1, 0, -1):
    	ret[i-1] += ret[i] // 10
    	ret[i] = ret[i] % 10
    return ret

A= 