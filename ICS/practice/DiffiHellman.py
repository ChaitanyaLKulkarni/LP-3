import socket
SERVER_PORT = 5566


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIP = input("Enter severIP: ")
    if serverIP == "":
        p = int(input("Enter p: "))
        g = int(input("Enter g: "))
        privateKey = int(input("Enter private key: "))
        publickey = pow(g, privateKey, p)

        sock.bind(("", SERVER_PORT))
        sock.listen(1)
        print("Waiting for client... ")

        conn, _ = sock.accept()
        conn.sendall(f"{p}|{g}|{publickey}".encode())
        otherPublicKey = int(conn.recv(1024).decode())
        print("Got other's public key:", otherPublicKey)

        sharedKey = pow(otherPublicKey, privateKey, p)
        print("Shared Key:", sharedKey)
        conn.close()
    else:
        sock.connect((serverIP, SERVER_PORT))
        data = sock.recv(1024).decode()
        p, g, otherPublicKey = map(int, data.split("|"))
        print(f"Got p: {p}, g: {g}, other's public key: {otherPublicKey}")
        privateKey = int(input("Enter private key: "))

        publickey = pow(g, privateKey, p)
        sock.sendall(f"{publickey}".encode())

        sharedKey = pow(otherPublicKey, privateKey, p)
        print("Shared key:", sharedKey)


if __name__ == '__main__':
    main()
