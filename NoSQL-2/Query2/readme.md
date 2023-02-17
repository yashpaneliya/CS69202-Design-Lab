# Query 2

For this query consider the files ‘access_log11.txt’ and ‘access_log12.txt’. Consider the network formed by the ip-addresses and the requested resources (only GET requests). An ip-address and a resource is considered connected then if and only if that resource was requested by the ip-address. Now, this connection among the ip-addresses and the resources form a network. Find the total number of unique pairs of ip-addresses which are disconnected from each other.

## Approach

### Mapper.py

1. Split the line and extract ip, resource name and request type
2. Check the type of resource and if it's a GET request then print the ip and resource name

### Combiner.py

1. Split the line and extract resource name and ip
2. Combine the resources requested by same ip and store it to dictionary of sets
3. Print the dictionary

### Reducer.py

1. Split the line and extract ip and resource list, put them in a dictionary of sets
2. Generate a dictionary of sets with resource name as key and list of ip that requested tha resource as value
3. Create a set unique resource name
4. Iterate over dictionary and check for intersection of ip between two resources in dictionary
5. If intersection found, merge the ip list into one and pop the other one from dictionary
6. Size of final dictionary will be the number of connected components
7. Calculate number of pairs according to size of lists in all remaining resources

## Steps to run

1. Put all the access_logXX.txt file in the folder
2. Run `make` in cmd
3. A result.txt file will be generated with desired output


## Parallel Processing

1. Logic remains same as above
2. Logic of mapper.py, combiner.py and reducer.py are converted to function
3. Pass each input file to mapper and generate its output parallely
4. Pass those output file to combiner and generate output file parallely
5. Pass those output files in reducer to generate final output
6. Record the total time