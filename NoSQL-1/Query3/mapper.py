import sys
import time


for line in sys.stdin:
    # Split the line into fields
    fields = line.strip().split()

    # Extract the relevant fields
    time_field = fields[3][1:]
    size = fields[9]

    # Convert the time field into a datetime object
    try:
        time_obj = time.strptime(time_field, "%d/%b/%Y:%H:%M:%S")
    except ValueError:
        continue

    # Convert the size field into an integer
    try:
        if size == "-":
            size = 0
        else:
            size = int(size)
    except ValueError:
        continue

    # Divide the time by 15*60 seconds to generate a unique key kind of value for each entry in a particular window
    window = int(time.mktime(time_obj) / 900)

    # Emit a key-value pair for this log entry
    print("%s\t%s" % (window, size))
