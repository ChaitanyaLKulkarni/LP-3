import math
import socket
from threading import Thread

SERVER_PORT = 5566


def gcd(a, b):
    while True:
        temp = a % b
        if temp == 0:
            return b
        a = b
        b = temp


class RSA:
    def __init__(self, conn):
        self.conn = conn
        self.recT = Thread(target=self.recv, daemon=True)
        self.recT.start()

        p = int(input("Enter p: "))
        q = int(input("Enter q: "))

        self.n = p * q
        phiOfN = (p-1) * (q-1)

        self.e = RSA.getEncryptionKey(phiOfN)
        self.d = RSA.getDecryptionKey(phiOfN, self.e)

        print(f"Private key: (d, n): ({self.d}, {self.n})")
        print(f"public Key: (e, n): ({self.e}, {self.n})")

        self.conn.sendall(f"{self.e}|{self.n}".encode())
        print("Enter msg to encrypt and send (< 0 to exit): ")
        while True:
            msg = int(input())
            if msg < 0:
                break
            self.send(msg)

    def send(self, msg):
        enc = pow(msg, self.other_e, self.other_n)
        self.conn.sendall(f"{enc}".encode())

    def recv(self):
        while True:
            data = self.conn.recv(1024).decode()
            if "|" in data:
                self.other_e, self.other_n = map(int, data.split("|"))
                print(
                    f"Got other's public key: (e, n): ({self.other_e}, {self.other_n})")
                continue
            print("----\nEncrypted msg:", data)
            dec = pow(int(data), self.d, self.n)
            print("Decrypted msg:", dec, "\n----")

    @staticmethod
    def getEncryptionKey(phiOfN):
        for i in range(2, phiOfN):
            if gcd(i, phiOfN) == 1:
                return i

    @staticmethod
    def getDecryptionKey(phiOfN, e):
        d = 0
        for i in range(1, phiOfN):
            d = (i * phiOfN + 1) / e
            if math.floor(d) == d:
                return int(d)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIP = input("Enter server ip: ")
    if serverIP == "":
        sock.bind(("", SERVER_PORT))
        sock.listen(1)
        print("Waiting for connection...")
        conn, _ = sock.accept()
        c = RSA(conn)
    else:
        sock.connect((serverIP, SERVER_PORT))
        c = RSA(sock)


if __name__ == '__main__':
    main()
