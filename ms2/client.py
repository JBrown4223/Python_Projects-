#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, os, sys, signal, argparse

IP = socket.gethostbyname('localhost')
PORT = 50000
ADDR = (IP, PORT)
SIZE = 2048
sockets = []
msgs = []
FORMAT = "utf-8"
DISCONNECT_MSG = "Disconnect"
menu = "Select a lottery and quantity -- (-l649) 649 (-lmax) LottoMax (-O49) Lottario"


# Fork and create the specified number of connections to the server


def connect(request):

    for requests in request:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockets.append(cs)
        msgs.append(requests)


    for socks in sockets:
        socks.connect(ADDR)

    for i in range(len(msgs)):
        cs = sockets[i]
        cs.send(msgs[i].encode(FORMAT))

    for cs in sockets:
        data = cs.recv(SIZE).decode(FORMAT)
        print(f"Received {cs.getsockname()}")
        print(data)
        if not data:
            print(f"Closing socket: {cs.getsockname()}")
            cs.close()


def main():
    parser = argparse.ArgumentParser("Client Request Handler")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-s', help="Use for a single connection")
    parser.add_argument('-m', help="Use for multiple connections with desired number of connections")

    arg = parser.parse_args()

    if arg.s:
        print(menu)
        request = []
        command = input(" ")
        request.append(command)
        connect(request)

    if arg.m:
        try:
            tot = sys.argv[2]
            tot_rqs = int(tot)
            request = []
            while tot_rqs > 0:
                print(menu + '\n')
                print(f"Commands Left: {tot_rqs}")
                command = input(" ")
                request.append(command)
                tot_rqs = tot_rqs - 1
        except OSError as e:
            m = f"Failed!: {e}"
            print(m)
            sys.exit(1)
        connect(request)

if __name__ == "__main__":
    main()
