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
        self.other_e = 0
        self.other_n = 0

        self.recvT = Thread(target=self.recv, daemon=True)
        self.recvT.start()

        p = int(input("Enter p: "))
        q = int(input("Enter q: "))

        self.n = p * q
        phiOfN = (p-1) * (q-1)

        self.e = RSA.getEncryptionKey(phiOfN)
        self.d = RSA.getDecryptionKey(phiOfN, self.e)
        print(f"Public Key (e, n) : ({self.e}, {self.n})")
        print(f"Private key (d, n) : ({self.d}, {self.n})")

        self.conn.sendall(f"{self.e}|{self.n}".encode())
        print("Enter msgs to send ( enter -ve to exit)")
        while True:
            msg = int(input())
            if(msg < 0):
                break
            self.send(msg)

    def send(self, msg):
        enc = pow(msg, self.other_e, self.other_n)
        self.conn.sendall(f"{enc}".encode())

    def recv(self):
        while True:
            data = self.conn.recv(1024)
            data = data.decode()
            if "|" in data:
                self.other_e, self.other_n = map(int, data.split("|"))
                print(
                    f"Received public key: (e, n): ({self.other_e, self.other_n})")
                continue
            print("----\nEncrpyed msg: ", data)
            msg = pow(int(data), self.d, self.n)
            print("Decrypted Msg: ", msg, "\n----")

    @staticmethod
    def getEncryptionKey(phiOfN):
        for i in range(2, phiOfN):
            if gcd(i, phiOfN) == 1:
                return i

    @staticmethod
    def getDecryptionKey(phiOfN, e):
        d = 0
        for i in range(1, 100):
            d = (i * phiOfN + 1) / e
            if math.floor(d) == d:
                return int(d)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIP = input("Enter server Ip: ")
    if serverIP == "":
        sock.bind(('', SERVER_PORT))
        sock.listen(1)
        print("Waiting..")
        conn, _ = sock.accept()
        c = RSA(conn)
        conn.close()
    else:
        sock.connect((serverIP, SERVER_PORT))
        print(f"Connected to : {serverIP}:{SERVER_PORT}")
        c = RSA(sock)
        sock.close()


if __name__ == '__main__':
    main()
