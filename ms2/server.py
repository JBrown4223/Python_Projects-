#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
#   Assignment:  MS2
#
#       Author:  Jonathan Brown
#     Language:  Python3
#   To Compile:  Set ./server.py and ./client.py to executables using chmod then use the following commands:
#                - ./server start - starts the daemon process and the socket listener
#                - ./client -s 1 for single execution | -m [number of executions]
#        Class:  Python for Programmers: Sockets and Security DPI912
#    Professor:  Harvey Kaduri
#     Due Date:  N/A
#    Submitted:  Really Late
#
# -----------------------------------------------------------------------------
#
#  Description:  A Non-Blocking Daemon server
#
# Collaboration:  N/A
#
#        Input:  The Server requires one additional argument ( start)
#                The Client requires 2 additional arguments (-s 1 | -m [n])
#
#       Output:  The Client interface will provide you with a print out of lotto tickets after you go through the
#       prompts.
#
#   Algorithm:  I used a double fork technique for both the daemon creation and the Lotto number generation
#
#
#   Required Features Not Included:
#
#   Known Bugs:  None that I am aware of
#
#   Classification: N/A
#
# ==============================================================================

import select, socket, os, sys, time

SIZE = 2048
FORMAT = "utf-8"
DISCONNECT_MSG = "Disconnect"
CONNECTED = True


def process(conn, input):
    log = open("/tmp/log.txt", 'a')
    log.write(f"Sub-Socket {conn.getsockname()} Opened At: " + time.ctime(time.time()) + '\n')
    log.close()
    pid3 = os.fork()
    if pid3 > 0:
        sys.exit(1)
    else:
        arg = "~/Downloads/lotto.py " + input
        os.system(arg)

    os.chdir("/tmp")
    os.setsid()
    os.umask(0)
    pid4 = os.fork()
    if pid4 > 0:
        sys.exit(1)

    else:
        outFile = open("/tmp/output.txt", "r")
        line = outFile.read()
        return line


def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(('localhost', 50000))
    server.listen(5)
    inputs = [server]
    outputs = []

    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)

            else:
                data = s.recv(SIZE).decode(FORMAT)
                if data:
                    log = open("/tmp/log.txt", 'a')
                    log.write(f"Request Received from :{s.getsockname()} " + time.ctime(time.time()) + '\n')
                    log.write(data+'\n')
                    log.close()
                    next_msg = process(s, data)
                    s.send(next_msg.encode(FORMAT))

                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)




try:
    pid = os.fork()
    if pid > 0:
        # Exit first parent.
        sys.exit(0)
except OSError as e:
    m = f"Fork #1 failed: {e}"
    print(m)
    sys.exit(1)
# Decouple from the parent environment.
os.chdir("/tmp")
os.setsid()
os.umask(0)
# Do second fork.
try:
    pid = os.fork()
    if pid > 0:
        # Exit from second parent.
        sys.exit(0)
except OSError as e:
    m = f"Fork #2 failed: {e}"
    print(m)
    sys.exit(1)

start()
