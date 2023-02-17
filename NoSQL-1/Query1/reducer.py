import sys

# variables to track current ip and its frequency
current_ip = ""
current_count = 0 

# reading lines from console
for line in sys.stdin:
    try:
        ip, count = line.strip().split("\t")
    except:
        continue

    try:
        count=int(count)
    except ValueError:
        continue

    # if we get a new ip then first print the current ip with its count
    # and then update current_ip with the recently scanned ip
    if current_ip != ip:
        if current_ip != "":
            print("{}\t{}".format(current_ip,current_count))
        current_ip = ip
        current_count=0
    # increment the frequency of current ip
    current_count += count

# print the last remaining ip
print("{}\t{}".format(current_ip,current_count))