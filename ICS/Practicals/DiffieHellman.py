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
import socket

SERVER_PORT = 1234


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIP = input("Enter server's IP: (leave blank) ")
    if serverIP != "":
        sock.connect((serverIP, SERVER_PORT))
        data = sock.recv(1024)
        print("Recieved ", data.decode())
        p, g, A = map(int, data.decode().split("|"))
        print("A =", A)
        bPrivate = int(input("Enter bob's private key (b): "))
        B = pow(g, bPrivate, p)
        print("B =", B)
        sock.send(str(B).encode())

        sharedKey = pow(A, bPrivate, p)
        print("Shared key =", sharedKey)
        sock.close()
        return

    p = int(input("Enter prime no. (p): "))
    g = int(input("Enter prime no. (g): "))
    aPrivate = int(input("Enter Alice's private key (a): "))
    A = pow(g, aPrivate, p)
    print("A =", A)

    sock.bind(('', SERVER_PORT))
    sock.listen(1)
    print("Waiting for connection")
    connection, addr = sock.accept()
    connection.sendall(f"{p}|{g}|{A}".encode())
    data = connection.recv(1024)
    B = int(data.decode())
    print("B =", B)

    sharedKey = pow(B, aPrivate, p)
    print("Shared key =", sharedKey)
    sock.close()


if __name__ == '__main__':
    main()
