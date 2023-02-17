# Query 1

For this query consider the files “access_log1.txt”, “access_log2.txt”, “access_log3.txt”, “access_log4.txt”, “access_log5.txt”, "access_log6.txt”, “access_log7.txt”, “access_log8.txt”, “access_log9.txt”, “access_log10.txt”. Find the average size (bytes) of every file type requested by the users. Files can be classified into the following types - image (.png, .jpg, .gif, .ico), video (.mp4, .flv), audio (.mp3) and webpage (.html, .css, .js, .php)

**Note:** The result will have lines such as: image 16.50 which means that the
average size of the requested image files is 16.50 bytes. Round the result to 2
decimal points. The output file should contain one such size in each line. The
ordering of the file types does not matter. In case of “-” in %b (size) consider the
size to be 0 bytes.

## Approach

### Mapper.py

1. Split the line and extract resource name and size
2. Check the type of resource and print the size with its type

### Combiner.py

1. Split the line and extract resource type and its size
2. According to type, increment the type count and total size of that type
3. Print type, final count and total size

### Reducer.py

1. Split the line and extract type, count and total size
2. Print the average of all types


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