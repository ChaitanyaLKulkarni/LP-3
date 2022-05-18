"""
    STEPS:
    1) Choose two (p, g) different large prime number
    2) select Alice secrete key (a)
    3) calculate A = g^a mod p
    4) send A to Bob
    5) Bob selects Bob secrete key (b)
    6) calculate B = g^b mod p
    7) send B to Alice
    8) Alice computes shared key (A^b mod p)
    9) Bob computes shared key (B^a mod p)
    10) Both Alice and Bob can use the shared key to encrypt and decrypt messages
"""


def main():

    p = int(input("Enter prime no. (p): "))
    g = int(input("Enter prime no. (g): "))

    aPrivate = int(input("Enter Alice's private key (a): "))
    A = pow(g, aPrivate, p)
    print("A =", A)

    # send p, g and A to Bob
    bPrivate = int(input("Enter Bob's private key (b): "))
    B = pow(g, bPrivate, p)
    print("B =", B)

    sharedKey = pow(A, bPrivate, p)
    print("Shared key(For Bob) =", sharedKey)

    # send B to Alice
    sharedKey = pow(B, aPrivate, p)
    print("Shared key(For Alice) =", sharedKey)


if __name__ == '__main__':
    main()
