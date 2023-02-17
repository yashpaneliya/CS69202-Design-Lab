# Mapper script
import sys

# Iterate through each log entry
for line in sys.stdin:
    # Split the line into fields
    fields = line.strip().split()
    ip = fields[0]
    size_str = fields[9]
    try:
        size = int(size_str) if size_str != "-" else 0
    except ValueError:
        continue
    # Output the IP address and the tuple (size, count)
    print("%s\t%s" % (ip, size))
