import socket

SERVER_PORT = 5566


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIp = input("Enter server IP(leave blank): ")
    if serverIp == "":
        print("Enter two prime numbers")
        p = int(input("Enter p: "))
        g = int(input("Enter g: "))
        privateKey = int(input("Enter Your private key: "))
        publicKey = pow(g, privateKey, p)

        sock.bind(("", SERVER_PORT))
        sock.listen(1)
        print("Waiting for client to connect...")
        conn, addr = sock.accept()
        print("Connected to: ", addr)
        print(f"Sending {p}(p), {g}(g) and {publicKey}(public key): ")
        conn.sendall(f"{p}|{g}|{publicKey}".encode())
        print("Waiting for client to send public key...")
        data = conn.recv(1024)
        otherPublicKey = int(data.decode())
        print(f"Received {otherPublicKey}")

        sharedKey = pow(otherPublicKey, privateKey, p)
        print(f"Got Shared key: ", sharedKey)
        conn.close()
    else:
        sock.connect((serverIp, SERVER_PORT))
        print("Connected to: ", serverIp)
        data = sock.recv(1024)
        p, g, otherPublicKey = map(int, data.decode().split("|"))
        print(f"Received {p}(p), {g}(g) and {otherPublicKey}(public key): ")
        privateKey = int(input("Enter Your private key: "))
        publicKey = pow(g, privateKey, p)
        print(f"Sending {publicKey}(public key): ")
        sock.sendall(f"{publicKey}".encode())
        sharedKey = pow(otherPublicKey, privateKey, p)
        print(f"Got Shared key: ", sharedKey)
        sock.close()


if __name__ == '__main__':
    main()
