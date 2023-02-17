# Reducer script
import sys

current_ip = None

# dictionary to store counts of ip and their object size list
counts = {}
sizes = {}

# Iterate through each key-value pair
for line in sys.stdin:
    try:
        ip, size = line.strip().split("\t")
        size = int(size)
    except ValueError:
        continue

    if current_ip is None:
        current_ip = ip
        counts[ip] = 1
        sizes[ip] = [size]
    # If the IP address has changed, check if the previous IP address meets the bot criteria
    elif current_ip != ip:
        if counts[current_ip] >= 10:
            flag = False
            for s in sizes[current_ip]:
                if s >= 1000:
                    flag=True
            if flag==False:
                print(current_ip)
        # updating the current variables with new arrived ip
        current_ip = ip
        counts[ip] = 1
        sizes[ip] = [size]
    else:
        # Update the current IP address, total count, and total size
        current_ip = ip
        counts[current_ip] = counts[current_ip] + 1
        sizes[current_ip].append(size)

# checking the last ip of the list for bot criteria
if counts[current_ip] >= 10:
    flag = False
    for s in sizes[current_ip]:
        if s >= 1000:
            flag=True
    if flag==False:
        print(current_ip)
