# Data extraction from logs using Mapper-Combiner-Reducer

## Problem statement

In the file “access_log.txt”, each line represents a hit to the Web server. It includes the IP address which accessed the site, the date and time of the access, and the name of the page which was visited.

The logfile is in the Common Log Format:

10.223.157.186 - - [15/Jul/2009:15:50:35 -0700] "GET /assets/js/lowpro.js HTTP/1.1" 200 10469

Queries to be implemented:
1. For this query consider the files “access_log1.txt”, “access_log2.txt”, “access_log3.txt”, “access_log4.txt”, “access_log5.txt”, “access_log6.txt”, “access_log7.txt”, “access_log8.txt”, “access_log9.txt”, “access_log10.txt”. Find the average size (bytes) of every file type requested by the users. Files can be classified into the following types - image (.png, .jpg, .gif, .ico), video (.mp4,.flv), audio (.mp3) and webpage (.html, .css, .js, .php)

2. For this query consider the files ‘access_log11.txt’ and ‘access_log12.txt’. Consider the network formed by the ip-addresses and the requested resources (only GET requests). An ip-address and a resource is considered connected then if and only if that resource was requested by the ip-address. Now, this connection among the ip-addresses and the resources form a network. Find the total number of unique pairs of ip-addresses which are disconnected from each other.

### With Multiprocessing
Perform same queries using multiprocessing.

## Code walk-through

- Each query contains a mapper, a combiner and a reducer file.
- The mapper file reads the input line by line and outputs the key-value pairs.
- The combiner file combines the key-value pairs with the same key.
- The reducer file reads the key-value pairs and outputs the result.
- Detailed information about the code is provided in separate query readmes of each query.

## How to run

1. Run the following command in the terminal:
    ```bash
	(cat access_log11.txt | python mapper.py | python combiner.py & cat access_log12.txt | python mapper.py | python combiner.py) | python reducer.py > result.txt
    ```
    Or if you are using Linux, run the following command inside the query directory:
    ```bash
    make
    ```
2. The result will be stored in the result.txt file.

## Output

- Query 2
```txt
28015
```