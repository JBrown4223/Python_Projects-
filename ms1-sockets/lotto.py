#!/usr/bin/python3
# ==============================================================================
#   Assignment:  Milestone 0
#
#       Author:  Jonathan Brown
#     Language:  Python, Imports: sys, argparse, and random
#   To Compile:  n/a
#
#        Class:  Python for Programmers: Sockets and Security (DPI912NSA.05037.2214)
#    Professor:  Harvey Kaduri
#     Due Date:  May 26th at 11:59pm
#    Submitted:  May 26th at 11:30pm
#
# -----------------------------------------------------------------------------
#
#  Description:  We were assigned the task of building a program that woul produce lottery numbers for the 3 most
#                popular lotteries. The program needed to take in command line arguments using argparse, and generate
#                generate the specified number of tickets
# Collaboration: No class collaboration but I consulted the Python documentation online as well as a few youtube videos
#
#        Input:  The program requires you to provide a lottery code and number of tickets you'd like to generate
#                  example - python3 lotto.py --O49 1 --- This would generate one ticket for Lottario
#
#       Output:  The Output identifies the lottery selected, the amount of number, and your new ticket.
#
#    Algorithm:  For the actual number generator the function requires a list of potential numbers and the number of
#                number of picks needed. I used a while loop that would run until the number threshold was met and I
#                used the built-in method pop() to remove each number selected to prevent doubling up. random.randInt
#                is used to pick a number between 1 and 49, this serves as the element that will extract the number
#                out of the list.
#   Required Features Not Included:  I think I satisfied all of the features but we'll find out I guess
#
#   Known Bugs:  Sometimes the program crashes because the list doesn't reset after running the program multiple times
#
#
#   Classification: N/A
#
# ==============================================================================


import sys
import argparse
import random
from daemonize import Daemonize



random.seed()

parser = argparse.ArgumentParser("Lottery Picking Program")
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--lotto649', nargs='+', help="Use 649 for Lotto 649 ticket generation")
parser.add_argument('--lottoMax', nargs='+', help="Use 649 for LottoMax ticket generation")
parser.add_argument('--O49', nargs='+', help="Use 049 for Lottoario ticket generation")

arg = parser.parse_args()

pid = "/temp/lotto.py.pid"


def lottoGen(numberPool, nums):
    # Assign the pool to a variable so global scope isn't lost from numberPool
    pool2 = numberPool
    # Array to store lotto numbers
    lottoTicket = []

    # This variable creates the ball effect
    highEnd = 49

    while nums > 0:
        r = random.randint(1, highEnd)  # 1 to 49
        l = pool2[r - 1]  # Accounts for the fact that Lists/Arrays start from 0
        pool2.pop(r - 1)  # Removes the element containing the selected number
        lottoTicket.append(l)
        nums = nums - 1
        highEnd = highEnd - 1

    lottoTicket.sort()
    print("Your Ticket is :" + str(lottoTicket))


if arg.lotto649:
    print(" 649: 6 numbers")
    nums = 6
    numberofTix = sys.argv[2]
    for i in range(int(numberofTix)):
        numberPool = [*range(1, 49)]
        lottoGen(numberPool, nums)

if arg.lottoMax:
    print(" LottoMax: 8 numbers")
    nums = 8
    numberofTix = sys.argv[2]
    for i in range(int(numberofTix)):
        numberPool = [*range(1, 49)]
        lottoGen(numberPool, nums)

if arg.O49:
    print(" Lottario: 6 numbers")
    nums = 6
    numberofTix = sys.argv[2]
    for i in range(int(numberofTix)):
        numberPool = [*range(1, 49)]
        lottoGen(numberPool, nums)

daemon = Daemonize(app="lotto", pid=pid, action=lottoGen)
daemon.start()
