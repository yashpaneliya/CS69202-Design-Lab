# Query 4

We define a bot as a client which have made atleast 10 requests to the server and all of the requested objects are of size less than 1000 bytes. Find the ip addresses of all the bots.

**Note:** The result will have lines such as: 10.223.157.186 which means that ip address 10.223.157.186 is a suspected bot. The output file should contain one such ip address in each line. The ordering of the ip addresses does not matter. In
case of “-” in %b (size) consider size to be 0 bytes.

## Approach

### Mapper.py

1. Reading the file line by line and takeing the 
2. Extracting the ip and content size from 0th and 9th index
3. Printing them tab-separated

### Reducer.py

1. Scanning the printed line from console and splitting at tab space
2. Create two dictionaries to store counts and sizes for each unique ips
3. if a new ip arrives then,
   1. First check previous ip's count is >= 10 and all the sizes recorded for that ip is less than 1000
   2. If true then print it
   3. update current ip with new ip and add it to dictionary
4. else increment the count in dictionary and append the size in list of that ip


## Steps to run

1. Put the access_log.txt file in the folder
2. Run `make` in cmd
3. A result.txt file will be generated with desired output