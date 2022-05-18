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
from threading import Thread

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
            print("e = ", i)
            return i


def getDecryptionKey(phiOfN, e):
    d = 0.0
    for i in range(1, phiOfN):
        d = float(i*phiOfN+1)/e
        if math.floor(d) == d:
            print("d =", d)
            break
    return int(d)


class Client:
    def __init__(self, connection, n, e, d) -> None:
        self.connection = connection
        self.n = n
        self.d = d
        self.e = e

        self.thread = Thread(target=self.recvThread, daemon=True)
        self.thread.start()

        self.connection.sendall(f"{self.n}|{self.e}".encode())
        while True:
            msg = int(input())
            self.send(msg)

    def send(self, msg):
        enc = pow(msg, self.other_e, self.other_n)
        self.connection.sendall(f"{enc}".encode())

    def recvThread(self):
        while True:
            data = self.connection.recv(1024)
            data = data.decode()
            if("|" in data):
                self.other_n = int(data.split("|")[0])
                self.other_e = int(data.split("|")[1])
                print(
                    f"GOT others public key (n, e) : ({self.other_n}, {self.other_e})")
                continue
            dec = pow(int(data), self.d, self.n)
            print("Encrypted msg:", data, "\tdecrypted msg:", dec)


def main():
    p = int(input("Enter prime no. (p): "))
    q = int(input("Enter prime no. (q): "))

    n = p * q
    phiOfN = (p - 1) * (q - 1)

    e = getEncryptionKey(phiOfN)
    d = getDecryptionKey(phiOfN, e)

    serverIp = input("Enter server ip: ")
    if serverIp != "":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((serverIp, SERVER_PORT))
        c = Client(sock, n, e, d)
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', SERVER_PORT))
    sock.listen(1)
    print("Waiting for client...")
    conn, addr = sock.accept()
    print("Connected to client")
    c = Client(conn, n, e, d)


if __name__ == '__main__':
    main()
