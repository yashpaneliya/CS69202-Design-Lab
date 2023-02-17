# Query 1

For every unique ip address, find the number of requests made to the server.

**Note:** The result will have lines such as: 10.223.157.186 10 which means that ip
address 10.223.157.186 has made 10 requests to the server. The output file
should contain one such count in each line. The ordering of the ip addresses
does not matter.

## Approach

### Mapper.py

1. IP addresses are on the zeroth index, so scanning each line of file, splitting it at " " and extracting first word
2. Printing it on console with a tab space and 1


### Reducer.py

1. Scanning the printed line from console and splitting at tab space
2. Now, I have to aggregate the same IPs and increment the count (i.e. frequency)
3. To check same ip, we already sorted the contents of mapper using sort command, so we take a string variable to keep track of current line (ip) and when incrementing the count until we get a new ip
4. as soon as we get a new IP, print the old ip and its count on the console


## Steps to run

1. Put the access_log.txt file in the folder
2. Run `make` in cmd
3. A result.txt file will be generated with desired output