# Command line chat application

This is a command line chat application that can be used to chat between two users on the same network. The application is written in C and uses sockets for communication between the two users. It supports multiple clients at a time and also supports group chat.

## Features supported

1. Handling multiple clients at a time
2. P2P messaging
3. Broadcast
4. Groups
    - Group formation (Permission and Permissionless)
    - Admin privileges (Add, remove, change admin, admin-only chat, etc.)
    - Group chat

## Code walk-through

### Server

- The server first creates a socket, binds it to the specified port and starts listening for incoming connections.
- Several structures are used to store the information about the clients and groups.
- When a client connects to the server, the server accepts the connection.
- The server then reads the request from the client and parses it.
- The server supports multiple clients at a time with the help of `select()` system call.
- The server then performs the required operation and sends the result back to the client.

### Client

- The client first creates a socket and connects to the server socket.
- The client then sends the request to the server.
- The client then reads the result from the server and prints it.

## Steps to run

### Server

To start the server, run the following command:

```bash
gcc 22CS60R70_server.c -o server
./server <PORTNUMBER>
```

### Client

To start the client, run the following command:

```bash
gcc 22CS60R70_client.c -o client
./client <PORTNUMBER>
```
*Open multiple terminals(or tabs) to create miltiple clients to chat*

### Bonus: Abusive text classification
- Integrated the abusive text classification model from Assignment 7 into the chat application. The model classifies the text as abusive or not and if it is abusive, it is not sent to the other user.
- If user tries to send abusive text more than 5 times, the user is blocked and removed from group.
- Server runs the model built using python libs using `execlp` system call and classifies the text as abusive or not.

*You can find detailed flow of working of each feature in the [report](/Chat%20app%20using%20Sockets/22CS60R70_Report.odt)*