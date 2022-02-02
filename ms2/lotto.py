#!/usr/bin/env python3
import sys
import os
import argparse
import random
import time

random.seed()

parser = argparse.ArgumentParser("Lottery Picking Program")
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-l649', help="Use for Lotto 649 ticket generation")
parser.add_argument('-lmax', help="Use for LottoMax ticket generation")
parser.add_argument('-O49', help="Use for Lottoario ticket generation")

arg = parser.parse_args()



def lottoGen(nums):
    # Assign the pool to a variable so global scope isn't lost from numberPool
    pool2 = [*range(1, 49)]
    # Array to store lotto numbers
    lottoTicket = []

    while nums > 0:
        r = random.randint(1, len(pool2))  # 1 to nth index
        l = pool2[r-1]
        if l >= 0 and l < len(pool2):
            lottoTicket.append(l)
            pool2.pop(r-1)  # Removes the element containing the selected number
            nums = nums - 1
        else:
            continue

    lottoTicket.sort()
    return lottoTicket


def main():
    if arg.l649:
        file = open("/tmp/output.txt", "w")
        numberofTix = sys.argv[2]
        file.write("Lotto 649: 6 numbers\n")
        nums = 6
        for i in range(int(numberofTix)):
            tix = lottoGen(nums)
            file.write(str(tix) + "\n")
        file.close()
    elif arg.lmax:
        file = open("/tmp/output.txt", "w")
        numberofTix = sys.argv[2]
        file.write("LottoMax: 8 numbers\n")
        nums = 8
        for i in range(int(numberofTix)):
            tix = lottoGen(nums)
            file.write(str(tix) + "\n")
        file.close()

    elif arg.O49:
        file = open("/tmp/output.txt", "w")
        numberofTix = sys.argv[2]
        file.write("Lottario 49: 6 numbers\n")
        nums = 6
        for i in range(int(numberofTix)):
            tix = lottoGen(nums)
            file.write(str(tix)+"\n")
        file.close()
    else:
        file = open("/tmp/output.txt", "w")
        line = "Process Started "
        file.write(line + time.ctime(time.time())+'\n')

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
os.chdir("/")
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

main()
