import numpy as np
import math
import random
import time

# 素数判定
def is_prime(q):
    q = abs(q)
    if q == 2: return True
    if q < 2 or q&1 == 0: return False
    return pow(2, q-1, q) == 1

# 離散ガウス分布から値をサンプルする
def randint_from_gaussian(size):
    x = np.random.normal(0, 1, size)
    return np.rint(x)

# 鍵生成
def gen_key(q, n, m):
    A = np.random.randint(q, size=(m, n))
    s = np.random.randint(q, size=n)
    e = randint_from_gaussian(m)
    b = (A.dot(s) + e) % q
    return A, s, b, e

# 暗号化
def enc(A, b, m, q, pt):
    S = [0, 0]
    if(m > 1):
        for i in range(2):
            S[i] = random.randint(i, m-1)

        if S[0] > S[1]:
            S[0], S[1] = S[1], S[0]
        if S[0] == S[1]:
            S[0] -= random.randint(1, S[0])

    c1 = 0
    c2 = pt * math.floor(q / 2)

    for i in range(S[0], S[1]+1):
        c1 += A[i, :]
        c2 += b[i]
    ct = [c1 % q, c2 % q]

    return ct

# 復号
def dec(ct, s, q):
    d = (ct[1] - ct[0].dot(s)) % q
    pt = 0
    if q/4 <= d and d <= 3*q/4:
        pt = 1

    return pt

# 正当性の検証
def correctness(ct, s, q, e, pt):
    d = (ct[1] - ct[0].dot(s)) % q
    test_d = sum(e) + pt*math.floor(q/2)
    if(d == test_d):
        print('correct!')
    else:
        print('incorrect')

if __name__=="__main__":
    n = int(input('n: '))

    q = int(input('q: '))
    if q < n**2 or 2 * n**2 < q:
        print('qの値が不正です。n^2≦q≦2n^2としてください')
        quit()
    elif not is_prime(q):
        print('qは素数にしてください')
        quit()

    m = int(input('m: '))
    pt1 = int(input('pt1: '))
    pt2 = int(input('pt2: '))

    A, s, b, e = gen_key(q, n, m)

    start_ct1 = time.time()
    ct1 = enc(A, b, m, q, pt1)
    end_ct1 = time.time()

    start_ct2 = time.time()
    ct2 = enc(A, b, m, q, pt2)
    end_ct2 = time.time()
    print('---encrypt result---')
    print(f'ct1: {ct1}, ct2: {ct2}')

    start_pt1 = time.time()
    result_pt1 = dec(ct1, s, q)
    end_pt1 = time.time()

    start_pt2 = time.time()
    result_pt2 = dec(ct2, s, q)
    end_pt2 = time.time()
    print('---decrypt result---')
    print(f'pt1: {result_pt1}, pt2: {result_pt2}')

    print('---time result---')
    print(f'ct1: {end_ct1 - start_ct1}s')
    print(f'ct2: {end_ct2 - start_ct2}s')
    print(f'pt1: {end_pt1 - start_pt1}s')
    print(f'pt2: {end_pt2 - start_pt2}s')

    print('---inspection result---')
    print('pt1:')
    correctness(ct1, s, q, e, pt1)
    print('pt2:')
    correctness(ct2, s, q, e, pt2)



