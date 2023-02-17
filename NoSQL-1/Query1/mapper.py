import sys

for line in sys.stdin:
    ip = line.strip().split()[0]
    print("{}\t1".format(ip))