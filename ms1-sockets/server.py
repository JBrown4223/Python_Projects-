#!/usr/bin/env python
# -*- coding: utf-8 -*-
from daemonize import Daemonize
import socket
import threading
import sys
import os

IP = socket.gethostbyname('localhost')
PORT = 5555
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "Disconnected"
menu = "Select a lottery -- (1) Lotto649 (2) LottoMax (3) Lottario (4) Disconnect"

def getTickets(arg1, arg2):

    output = os.system(f"python3 lotto.py {arg1} {arg2}")
    sys.stdout = output
    return sys.stdout


def handle_client(conn, addr):
    print(f"---New Connection Made {addr} --- ")
    connected = True
    while connected:
        conn.send(menu.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == "4":
            msg = f"Client with address {addr} disconnected"
            conn.send(msg.encode(FORMAT))
            break
        elif msg == "1":
            resp = "How many 649 tickets would you like?"
            conn.send(resp.encode(FORMAT))
            resp = conn.recv(SIZE)
            # Get Tickets Function
            msg = getTickets("--l649", resp)
            conn.send(msg.encode(FORMAT))
        elif msg == "2":

            resp = "How many LottoMax tickets would you like?"
            conn.send(resp.encode(FORMAT))
            resp = conn.recv(SIZE)
            # Get Tickets Function
            msg = getTickets("--lottoMax", resp)
            conn.send(msg.encode(FORMAT))
        elif msg == "3":
            resp = "How many LottoMax tickets would you like?"
            conn.send(resp.encode(FORMAT))
            resp = conn.recv(SIZE)
            msg = getTickets("--049", resp)
            conn.send(msg.encode(FORMAT))
    conn.close()
    sys.exit(1)

def main():
    print("--- Starting up ----")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"--- Ready to Accept Connections on {IP}:{PORT} ---")

    while True:
        conn, addr = server.accept()

        # Separate thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active Connections: {threading.activeCount() - 1}")


if __name__ =="__main__":
    main()