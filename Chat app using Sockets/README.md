# Command line chat application

This is a command line chat application that can be used to chat between two users on the same network. The application is written in C and uses sockets for communication between the two users. It supports multiple clients at a time and also supports group chat.

## Usage

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

## Features supported

1. Handling multiple clients at a time
2. P2P messaging
3. Broadcast
4. Groups
    - Group formation (Permission and Permissionless)
    - Admin privileges (Add, remove, change admin, admin-only chat, etc.)
    - Group chat

### Bonus: Abusive text classification
- Integrated the abusive text classification model from Assignment 7 into the chat application. The model classifies the text as abusive or not and if it is abusive, it is not sent to the other user.
- If user tries to send abusive text more than 5 times, the user is blocked and removed from group.

*You can find detailed flow of working of each feature in the [report](/Chat%20app%20using%20Sockets/22CS60R70_Report.odt)*