# Query 2

Find the top-10 requested image files (png, jpg, gif, ico) by the clients.

**Note:** The result will have lines such as: /assets/img/loading.gif 12 which means
that the resource file /assets/img/loading.gif was requested 12 times by the
clients. The ordering withing these top-10 resource files does not matter. The
output file should contain 10 such lines

## Approach

### Mapper.py

1. Reading the file line by line and takeing the 6th indexed word/string from the line as it contains the requested resource
2. Check if the word/string has an image file extension usinf regex
3. If yes then print it with appending a tab-space and "1"


### Reducer.py

1. Scanning the printed line from console and splitting at tab space
2. Create a list to keep track of most frequent images
3. for each scanned line, check if it is the same image as current image, if yes then just increment the count
4. Else, 
   1. If length of list is less than 10 then directly append it and reset the current image and count variable
   2. Else, check if the count of last image in list is greater than current incoming image, if not then replace it with current incoming image and rearrange the list according to counts
5. Append the last scanned image with its count


## Steps to run

1. Put the access_log.txt file in the folder
2. Run `make` in cmd
3. A result.txt file will be generated with desired output