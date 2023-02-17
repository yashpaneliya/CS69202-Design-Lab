# Query 3

For every 15 minute window, find the window with the maximum server load with respect to the size of the objects returned to the clients. You need to print the total size (bytes) of the returned objects by the server in the window with the maximum load.

**Note:** The output file should contain the size of the returned objects in bytes printed on a single line. In case of “-” in %b (size) consider size to be 0 bytes

## Approach

### Mapper.py

1. Reading the file line by line and takeing the 
2. Extracting time field and size of object from 3rd and 9th index of splitted line
3. Convert time string into date time object
4. Convert datetime object to seconds from epoch time
5. Divide the time by 15*60 seconds to generate a unique key kind of value for each entry in a particular window
6. Print it with the object size

### Reducer.py

1. Scanning the printed line from console and splitting at tab space
2. Check if the key generated from mapper is same as current key then keep adding the size in current size
3. As soon as, we get the new key, check whether previous total size of key greater than maxsize or not and update mazsize accordingly

## Steps to run

1. Put the access_log.txt file in the folder
2. Run `make` in cmd
3. A result.txt file will be generated with desired output