import socket


IP = socket.gethostbyname('localhost')
PORT = 5555
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "Disconnected"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"--- Client Connected to Server at {IP}:{PORT} ---")

    connected = True
    while connected:
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"Server : {msg}")
        msg = input("> ")
        client.send(msg.encode(FORMAT))
        if msg.__contains__(DISCONNECT_MSG):
            client.close()
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"Server : {msg}")

if __name__=="__main__":
    main()
