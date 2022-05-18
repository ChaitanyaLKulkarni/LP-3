"""
    STEPS:
    1) Choose two (p, q) different large prime number
    2) calculate n = p * q
    3) calculate phi(n) = (p - 1) * (q - 1)
    4) Choose e, 1 < e < phi(n) such that gcd(e, phi(n)) = 1
    5) calculate d = e^-1 mod phi(n)

    e,n = public key
    d,n = private key

"""
import math


def gcd(a, b):
    while True:
        temp = a % b
        if temp == 0:
            return b
        a = b
        b = temp


def getEncryptionKey(phiOfN):
    for i in range(2, phiOfN):
        if gcd(phiOfN, i) == 1:
            return i


def getDecryptionKey(phiOfN, e):
    d = 0
    for i in range(1, 100):
        d = (i*phiOfN+1) / e
        if math.floor(d) == d:
            break
    return int(d)


def main():

    p = int(input("Enter prime no. (p): "))
    q = int(input("Enter prime no. (q): "))

    n = p * q
    phiOfN = (p - 1) * (q - 1)

    e = getEncryptionKey(phiOfN)
    d = getDecryptionKey(phiOfN, e)

    print(f"\np = {p}\tq= {q}")
    print(f"n = {n}\tphi(n) = {phiOfN}")
    print(f"Public Key(e) = {e}")
    print(f"Private Key(d) = {d}")

    while True:
        msg = int(input("\nEnter Msg(0 to quit): "))
        if msg == 0:
            break
        enc = pow(msg, e, n)  # using public key
        print("encrypted message:", enc)
        dec = pow(enc, d, n)  # using private key
        print("decrypted message:", dec)


if __name__ == '__main__':
    main()
