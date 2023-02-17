import sys

# Keep track of the current image and the total number of requests
current_image = None
current_count = 0

# Use a list to store the top-10 results
img_list = []

# Read input from stdin
for line in sys.stdin:
    # Extract the key-value pair
    image, count = line.strip().split("\t")
    try:
        count = int(count)
    except ValueError:
        continue

    # If the image has changed, add the result for the previous image to the top-10 list
    if current_image and current_image != image:
        if len(img_list) < 10:
            img_list.append((current_image, current_count))
        else:
            # Check if the current count is greater than the lowest count in the list
            lowest_count = img_list[-1][1]
            if current_count > lowest_count:
                img_list[-1] = (current_image, current_count)

                # Re-sort the list in descending order based on count
                for i in range(len(img_list) - 1, 0, -1):
                    if img_list[i][1] > img_list[i-1][1]:
                        img_list[i], img_list[i-1] = img_list[i-1], img_list[i]
                    else:
                        break
        current_count = 0

    # Update the current image and total count
    current_image = image
    current_count += count

# Add the result for the last image to the top-10 list
if len(img_list) < 10:
    img_list.append((current_image, current_count))
elif current_count > img_list[-1][1]:
    img_list[-1] = (current_image, current_count)

# Print the top-10 results
for image, count in img_list:
    print("%s\t%s" % (image, count))
