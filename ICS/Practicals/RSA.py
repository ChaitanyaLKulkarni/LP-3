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
import socket

SERVER_PORT = 1234


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
    d = 0.0
    for i in range(1, 100):
        d = float(i*phiOfN+1)/e
        if math.floor(d) == d:
            print("i =", i, "d =", d)
            break
    return int(d)


def main():

    serverIP = input("Enter server's IP: (leave blank) ")
    if serverIP != "":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((serverIP, SERVER_PORT))

        data = sock.recv(1024)
        data = data.decode()
        print("received message:", data)
        n, e = map(int, data.split("|"))

        while True:
            msg = int(input("Enter msg to send (0 to quit) : "))
            if(msg == 0):
                break
            enc = pow(msg, e, n)
            print("encrypted message:", enc)
            sock.sendall(f"{enc}".encode())
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', SERVER_PORT))
    sock.listen(5)

    p = int(input("Enter prime no. (p): "))
    q = int(input("Enter prime no. (q): "))
    n = p * q
    phiOfN = (p - 1) * (q - 1)

    e = getEncryptionKey(phiOfN)
    d = getDecryptionKey(phiOfN, e)

    print(f"p = {p}\tq= {q}")
    print(f"n = {n}\tphi(n) = {phiOfN}")
    print(f"Public Key(e) = {e}")
    print(f"Private Key(d) = {d}")

    print("\n---Waiting for connection---")
    connection, client_address = sock.accept()

    print(f"\nSending public key to {client_address}")
    connection.sendall(f"{n}|{e}".encode())
    print("Public key sent")

    while True:
        data = connection.recv(1024)
        print("encrypted message:", data.decode())
        data = int(data.decode())
        print("decrypted message:", pow(data, d, n))

    # print("encrypted message:", pow(data, e, n))
    # print("decrypted message:", pow(data, d, n))

    # pt = int(input("Enter plain text: "))
    # ct = pow(pt, e, n)
    # print(f"Cipher text = {ct}")

    # dt = pow(ct, d, n)
    # print(f"Decrypted text = {dt}")


if __name__ == '__main__':
    main()
