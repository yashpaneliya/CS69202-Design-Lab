# Socket Programming

## Problem Statement

Write two separate C program, one for TCP server (handles request for single user) and other one for client.

The server should parse the string received from the client, which will contain the following requests in the given format:
1. NUMROW: Returns the total number of rows in the file. This is a helper command for the client to know the total no. of students info present in the file.

2. INSERT <message>: Inserts the string specified in message to the end of the file. The message should be in the format as specified below-:
<Roll_No.>[TAB]<Student_Name>[TAB]<A_1>.[TAB]......[TAB]<A_5>

3. AVERAGE <Assignment No.>: Returns the average of all the marks for specified assignment number.

4. GRADEX <Roll_No.>: Returns the student details of the specified roll

5. SORTX <field> <start_row> <end_row> : Sort according to the given field (field can be either R,S,A_1,A_2....A_5 indicating roll_no.,stu_name and assignments marks respectively) as specified-:
    - If only the field is mentioned then sort all the rows with respect to the field.
    - If only start_row is mentioned then sort all the rows from start_row to the end of the file w.r.t the given field.
    - Otherwise,sort the rows from start_row to end_row w.r.t the given field.
2. RANKX <Roll_No.>: Returns the rank of the specified roll no. along with the student details. If roll number is not specified then return the top 10 student details in the order of their rank.
3. SIMILARX <Assignment No.>: Returns the student details(roll number and student name) who are having similar marks for the given assignment number. You should also return the marks for those students

The client establishes a connection with the server socket on the specified port. Then, it passes NUMROW,INSERT,AVERAGE,GRADEX,EXIT requests to the server

## Code walk-through

### Server

- The server first creates a socket, binds it to the specified port and starts listening for incoming connections.
- When a client connects to the server, the server accepts the connection.
- The server then reads the request from the client and parses it.
- The server then performs the required operation and sends the result back to the client.

### Client

- The client first creates a socket and connects to the server socket.
- The client then sends the request to the server.
- The client then reads the result from the server and prints it.

## Steps to run

- Compile the server and client programs using the following commands:
    - `gcc server.c -o server`
    - `gcc client.c -o client`
- Run the server using the following command:
    - `./server` (The server will listen on port 5000)
- Run the client using the following command:
    - `./client`