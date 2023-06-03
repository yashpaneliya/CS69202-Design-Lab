# Data extraction from logs using Mapper-Reducer

## Problem statement

In the file “access_log.txt”, each line represents a hit to the Web server. It includes the IP address which accessed the site, the date and time of the access, and the name of the page which was visited.

The logfile is in the Common Log Format:

10.223.157.186 - - [15/Jul/2009:15:50:35 -0700] "GET /assets/js/lowpro.js HTTP/1.1" 200 10469

Queries to be implemented:
1. For every unique ip address, find the number of requests made to the server
2. Find the top-10 requested image files (png, jpg, gif, ico) by the clients
3. For every 15 minute window, find the window with the maximum server load with respect to the size of the objects returned to the clients. You need to print the total size (bytes) of the returned objects by the server in the window with the maximum load.
4. We define a bot as a client which have made atleast 10 requests to the server and all of the requested objects are of size less than 1000 bytes. Find the ip addresses of all the bots.

## Code walk-through

- Each query contains a mapper and a reducer file.
- The mapper file reads the input line by line and outputs the key-value pairs.
- The reducer file reads the key-value pairs and outputs the result.
- Detailed information about the code is provided in separate query readmes of each query.

## How to run

1. Run the following command in the terminal:
    ```bash
    cat access_log.txt | python mapper.py | sort | python reducer.py > result.txt
    ```
    Or if you are using Linux, run the following command inside the query directory:
    ```bash
    make
    ```
2. The result will be stored in the result.txt file.

## Output

- Query 1
```txt
10.100.100.114	1
10.100.100.142	1
10.100.100.191	1
10.100.100.80	19
10.100.101.113	4
10.100.101.181	2
...
```