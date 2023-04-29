#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdbool.h>
#include <signal.h>

volatile sig_atomic_t termination_flag = 0;

/////////////////////////////////////////////////////////////////////////
//                             ID: 22CS60R70                           //
//                              CLIENT CODE                            //
//      How to run?                                                    //
//      - gcc 22CS60R70_A7_P1_client.c -o client                       //
//      - ./client                                                     //
//                                                                     //
/////////////////////////////////////////////////////////////////////////

void error(char *msg)
{
    perror(msg);
    exit(0);
}

void sigterm_handler(int sig)
{
    exit(0);
}

int sockfd;

void sigChandler(int sig_num)
{
    if (sig_num == SIGINT)
    {
        char message[256];
        bzero(message, 256);
        sprintf(message, "/quit");
        send(sockfd, message, sizeof(message), 0);
    }
}

void sigZhandler(int sig_num)
{
    if (sig_num == SIGTSTP)
    {
        char message[256];
        bzero(message, 256);
        sprintf(message, "/quit");
        send(sockfd, message, sizeof(message), 0);
    }
}

int main(int argc, char *argv[])
{
    signal(SIGINT, sigChandler); // handles ^C
    signal(SIGTSTP, sigZhandler); // handles ^C

    int portno = 9034;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    struct hostent *server;
    server = gethostbyname("127.0.0.1");

    if (server == NULL)
    {
        fprintf(stderr, "ERROR, no such host");
        exit(0);
    }

    struct sockaddr_in serv_addr;
    bzero((char *)&serv_addr, sizeof(serv_addr)); // initializes buffer
    serv_addr.sin_family = AF_INET;               // for IPv4 family
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(atoi(argv[1])); // defining port number

    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        error("ERROR connecting\n");
    }

    char buffer[256];

    bzero(buffer, 256);
    int n; // client buffer to forward request to the server

    int myid, serversock;
    char *trash;

    if ((n = read(sockfd, buffer, sizeof(buffer))) != 0)
    {
        if (strcmp(buffer, "Connection limit reached! Try again later.") == 0)
        {
            printf("%s\n", buffer);
            close(sockfd);
            return 0;
        }
    }

    sscanf(buffer, "%[^:]:%d%[^:]:%d", trash, &myid, trash, &serversock);
    printf("My ID: %d\n", myid);

    printf("=========================================================\n");
    printf("=\t\tAVAILABLE COMMANDS\t\t\t=\n");
    printf("=\t1. /active : print all online clients\t\t=\n");
    printf("=\t2. /send ID MSG : send message to a client\t=\n");
    printf("=\t3. /broadcast MSG : broadcast message to all\t=\n");
    printf("=\t4. /quit : terminate client\t\t\t=\n");
    printf("=========================================================\n");

    bool flag = true;
    int pid;

    if ((pid = fork()) == 0)
    {
        while (1)
        {
            bzero(buffer, 256);
            fgets(buffer, 256, stdin);
            n = write(sockfd, buffer, sizeof(buffer));
        }
        close(sockfd);
    }
    else
    {
        bzero(buffer, 256);
        while ((n = read(sockfd, buffer, sizeof(buffer))) != 0)
        {
            if (strncmp(buffer, "500", 3) == 0)
            {
                kill(pid, SIGTERM);
                close(sockfd);
                exit(0);
            }

            printf("%s\n", buffer);
            bzero(buffer, 256);
        }
    }
    return 0;
}
