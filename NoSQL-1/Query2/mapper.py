import sys
import re

# Define the regex pattern for image file extensions
pattern = re.compile(r'\.(png|jpg|gif|ico)$', re.IGNORECASE)

# Read input from stdin
for line in sys.stdin:
    try:
        # Split the log entry into fields
        fields = line.strip().split()

        # Check if the requested resource is an image file
        resource = fields[6]
    except Exception as e:
        # Catch any exceptions that occur while accessing fields[6] and continue to the next iteration
        continue
    
    try:
        if pattern.search(resource):
            print("%s\t%s" % (resource, 1))
    except Exception as e:
        # Catch any exceptions that occur while searching for pattern and continue to the next iteration
        continue
