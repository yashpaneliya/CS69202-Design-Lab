#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

/////////////////////////////////////////////////////////////////////////
//                             ID: 22CS60R70                           //
//                              CLIENT CODE                            //
//      How to run?                                                    //
//      - gcc client2.c -o client                                      //
//      - ./client                                                     //
//                                                                     //
/////////////////////////////////////////////////////////////////////////


void error(char *msg)
{
  perror(msg);
  exit(0);
}

int main(int argc,char *argv[])
{
    int sockfd, portno=5000;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    struct hostent *server;
    server = gethostbyname("127.0.0.1");

    if (server == NULL)
    {
        fprintf(stderr,"ERROR, no such host");
        exit(0);
    }

    struct sockaddr_in serv_addr;
    bzero((char *) &serv_addr, sizeof(serv_addr)); // initializes buffer
    serv_addr.sin_family = AF_INET; // for IPv4 family
    bcopy((char *)server->h_addr, (char *) &serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(portno); //defining port number
    
    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0)
    {
         error("ERROR connecting\n");
    }

    char buffer[256];
    while(1)
    {
        printf("> Enter the command (EXIT to terminate):\n");
        bzero(buffer,256);
        int n; // client buffer to forward request to the server

        fgets(buffer,256,stdin);

        n=write(sockfd,buffer,sizeof(buffer));
        bzero(buffer, 256);
    
        // looping till server sends completion
        while((n=read(sockfd,buffer,sizeof(buffer)))!=0)
        {
            // Request processed indicator
            if(strcmp(buffer,"done")==0)
            {
                break;
            }
            // Termination indicator
            if(strncmp(buffer,"CONNECTION TERMINATED",21)==0)
            {
                break;
            }
            printf("%s\n",buffer);
        }
        // Termination indicator
        if(strncmp(buffer,"CONNECTION TERMINATED",21)==0)
        {
            printf("***SUCCESSFUL TERMINATION***\n");
            break;
        }
    }
    close(sockfd);
    return 0;
}
