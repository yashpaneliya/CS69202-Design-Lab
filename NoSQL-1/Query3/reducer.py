import sys

# Keep track of the current window and the total size of the objects
current_window = None
current_size = 0
max_size = 0

# Read input from stdin
for line in sys.stdin:
    # Extract the key-value pair
    window, size = line.strip().split("\t")
    window = int(window)
    size = int(size)
    # If the current window is None, initialize it and the current size
    if current_window is None:
        current_window = window
        current_size = size
    # If the window has changed, update the maximum size if necessary
    elif current_window != window:
        if current_size > max_size:
            max_size = current_size
        current_window = window
        current_size = size
    # Otherwise, add the size to the current size
    else:
        current_window = window
        current_size += size

# Update the maximum size for the last window
if current_size > max_size:
        max_size = current_size
        current_size = 0

# Print the maximum size
print(max_size)