#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <time.h>
#include <stdbool.h>
#include <wait.h>

#define PORT "9034" // port we're listening on
/////////////////////////////////////////////////////////////////////////
//                             ID: 22CS60R70                           //
//                              SERVER CODE                            //
//      How to run?                                                    //
//      - gcc 22CS60R70_A7_P1_server.c -o server                       //
//      - ./server                                                     //
//                                                                     //
/////////////////////////////////////////////////////////////////////////
struct client
{
    int id;
    int socketfd;
    int grpCount;
    int joinedGroups[128];
    int abuseCount;
};
struct client *clientList[10];

struct message
{
    int from;
    int to;
    char *message;
};

struct Group
{
    int groupid;        // unique group-id
    int membersid[5];   // members of group
    int tempMembers[4]; // pending member requests
    bool isCreated;     // group is active or not
    int grpsize;        // no. of members
    int reqSize;        // no. of request sent
    int admins[5];      // id of admins
    int adminlen;       // no. of admins
    bool isBroadcast;   // admin-only or not
};
struct Group groups[128];
int grpIndex = 0;

struct AdminRequest
{
    int grpid;
    int posCount;
    int negCount;
    int totalAdmins;
    int memberid;
    bool status;
};
struct AdminRequest adminRequests[100];
int admReqIndex = 0;
// get client id from records
int getClientId(int clientfd)
{
    int sender;
    for (int i = 0; i < 10; i++)
    {
        if (clientList[i] != NULL && clientList[i]->socketfd == clientfd)
        {
            sender = clientList[i]->id;
            return sender;
        }
    }
    return -1;
}
// get client fd from records
int getClientFD(int clientid)
{
    int sender;
    for (int i = 0; i < 10; i++)
    {
        if (clientList[i] != NULL && clientList[i]->id == clientid)
        {
            sender = clientList[i]->socketfd;
            return sender;
        }
    }
    return -1;
}
// check whether a client exist or not
int isClient(int clientid)
{
    for (int i = 0; i < 10; i++)
    {
        if (clientList[i] != NULL && clientList[i]->id == clientid)
        {
            return 1;
        }
    }
    return 0;
}
// get index of group in records
int getGroupIndex(int grpid)
{
    for (int i = 0; i < grpIndex; i++)
    {
        if (groups[i].groupid == grpid)
            return i;
    }
    return -1;
}
// authority function
int isAdmin(int _grpindex, int adminid)
{
    for (int i = 0; i < 5; i++)
    {
        if (groups[_grpindex].admins[i] == adminid)
            return 1;
    }
    return 0;
}
// membership function
int isMember(int _grpindex, int clientid)
{
    for (int i = 0; i < 5; i++)
    {
        if (groups[_grpindex].membersid[i] == clientid)
            return 1;
    }
    return 0;
}
// request checker
int isInvited(int _grpindex, int clientid)
{
    for (int i = 0; i < 4; i++)
    {
        // printf("Temp: %d\n",groups[_grpindex].tempMembers[i]);
        if (groups[_grpindex].tempMembers[i] == clientid)
            return 1;
    }
    return 0;
}
// check whether a group is still active or not
bool isActiveGroup(int grpid)
{
    int _grpindex = getGroupIndex(grpid);
    if (_grpindex == -1)
        return false;
    return groups[_grpindex].isCreated;
}
// function to generate 5 digit random id for client
int generateRandomId()
{
    srand(time(NULL)); // Seed the random number generator with current time
    int random_num = rand() % 90000 + 10000;
    return random_num;
}
// function to generate 3 digit random id for group
int generateRandomGrpId()
{
    srand(time(NULL)); // Seed the random number generator with current time
    int random_num = rand() % 900 + 100;
    return random_num;
}
void logger(char *log_message, ...)
{
    va_list args;
    va_start(args, log_message);
    vfprintf(stderr, log_message, args);
    va_end(args);
}
// send message in group
void sendGroup(char *message, int groupid, int clientfd)
{
    char buffer[256];
    int _grpindex = getGroupIndex(groupid);
    if (_grpindex == -1)
    {
        bzero(buffer, 256);
        sprintf(buffer, "Group does not exist!\n");
        send(clientfd, buffer, sizeof(buffer), 0);
        return;
    }

    if (groups[_grpindex].isCreated == false)
    {
        bzero(buffer, 256);
        sprintf(buffer, "The group is not created yet! Waiting for everyone's response");
        send(clientfd, buffer, sizeof(buffer), 0);
        return;
    }

    int clientid = getClientId(clientfd);
    if (isMember(_grpindex, clientid) == 0)
    {
        bzero(buffer, 256);
        sprintf(buffer, "You are not a member of this group\n");
        send(clientfd, buffer, sizeof(buffer), 0);
        return;
    }

    if (groups[_grpindex].isBroadcast == true && isAdmin(_grpindex, clientid) == 0)
    {
        bzero(buffer, 256);
        sprintf(buffer, "It's a admin-only group. You can't send message to this group\n");
        send(clientfd, buffer, sizeof(buffer), 0);
        return;
    }

    pid_t pid = 0;
    int status;
    char *arglist[] = {"python3", "exam.py", message, NULL};
    pid = fork();
    if (pid == 0)
    {
        // printf("I am the child.\\n");
        execvp("python3", arglist);
        perror("In exec(): ");
    }
    if (pid > 0)
    {
        // printf("I am the parent, and the child is %d.\\n", pid);
        pid = wait(&status);
        FILE *fptr;

        fptr = fopen("res.txt", "r");
        char line[100]; // buffer to hold each line
        fgets(line, sizeof(line), fptr);
        puts(line);

        if (strncmp(line, "hate_abusive", 12) == 0)
        {
            char buf[512];
            bzero(buf, 512);
            sprintf(buf, "Sent abusive message. !!Msg  locked!!");
            send(clientfd, buf, sizeof(buf), 0);
            printf("Message hasn't been sent to client because of abusiveness!!\n");
            clientList[clientfd % 10]->abuseCount++;
            if (clientList[clientfd % 10]->abuseCount >= 5)
            {
                removeRecClient(clientfd);
            }
            return;
        }
        // printf("End of process %d: ", pid);
        if (WIFEXITED(status))
        {
            printf("The process ended with exit(%d).\\n", WEXITSTATUS(status));
        }
        if (WIFSIGNALED(status))
        {
            printf("The process ended with kill -%d.\\n", WTERMSIG(status));
        }
    }
    if (pid < 0)
    {
        perror("In fork():");
    }

    int senderId = getClientId(clientfd);
    for (int i = 0; i < groups[_grpindex].grpsize; i++)
    {
        if (groups[_grpindex].membersid[i] != senderId)
        {
            bzero(buffer, 256);
            sprintf(buffer, "[Group %d : Sender : %d] %s", groupid, senderId, message);
            send(getClientFD(groups[_grpindex].membersid[i]), buffer, sizeof(buffer), 0);
        }
    }
}
// function to make a normal group
void makeGroup(char *request, int adminfd)
{
    char req[32];
    int adminid = getClientId(adminfd);

    // intializing group props
    groups[grpIndex].groupid = generateRandomGrpId();
    groups[grpIndex].membersid[0] = adminid;
    // first admin is calling client
    groups[grpIndex].admins[0] = adminid;
    groups[grpIndex].adminlen = 1;
    groups[grpIndex].isCreated = true;
    groups[grpIndex].isBroadcast = false;

    char message[256];

    int argcount = sscanf(request, "%s %d %d %d %d\n", req, &groups[grpIndex].membersid[1], &groups[grpIndex].membersid[2], &groups[grpIndex].membersid[3], &groups[grpIndex].membersid[4]);

    if (argcount == 1)
    {
        bzero(message, 256);
        sprintf(message, "Please provide member ids\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    groups[grpIndex].grpsize = 1;
    groups[grpIndex].adminlen = 1;
    // incrementing group count of admin client
    clientList[adminfd % 10]->joinedGroups[clientList[adminfd % 10]->grpCount++] = groups[grpIndex].groupid;

    for (int i = 1; i < argcount; i++)
    {
        int fd = getClientFD(groups[grpIndex].membersid[i]);
        if (fd != -1)
        {
            bzero(message, 256);
            sprintf(message, "[Group %d Admin: %d] : You are added in the group.\n", groups[grpIndex].groupid, adminid);
            send(fd, message, sizeof(message), 0);
            // Insert group id in client object
            clientList[fd % 10]->joinedGroups[clientList[fd % 10]->grpCount++] = groups[grpIndex].groupid;
            // puts(message);
            (groups[grpIndex].grpsize)++;
        }
        else
        {
            bzero(message, 256);
            sprintf(message, "**Member with id %d does not exist**\n", groups[grpIndex].membersid[i]);
            // sprintf(message, "You are added in a group %d by %d\n", groups[grpIndex].groupid, adminid);
            send(fd, message, sizeof(message), 0);
        }
    }
    bzero(message, 256);
    sprintf(message, "**Group created with id %d**\n", groups[grpIndex].groupid);
    send(adminfd, message, sizeof(message), 0);
    grpIndex++;
}
// send request to join the group
void makeGroupReq(char *request, int adminfd)
{
    char req[32];
    int adminid = getClientId(adminfd);

    // intializing group props
    groups[grpIndex].groupid = generateRandomGrpId();
    groups[grpIndex].membersid[0] = adminid;
    // first admin is calling client
    groups[grpIndex].admins[0] = adminid;
    groups[grpIndex].isCreated = false;
    groups[grpIndex].isBroadcast = false;
    groups[grpIndex].reqSize = 0;

    // incrementing group count of admin client
    clientList[adminfd % 10]->joinedGroups[clientList[adminfd % 10]->grpCount++] = groups[grpIndex].groupid;

    char message[256];
    // extracting ids to whom we send join request
    int argcount = sscanf(request, "/makegroupreq %d %d %d %d\n", &groups[grpIndex].tempMembers[0], &groups[grpIndex].tempMembers[1], &groups[grpIndex].tempMembers[2], &groups[grpIndex].tempMembers[3]);

    if (argcount == 1)
    {
        bzero(message, 256);
        sprintf(message, "Please provide member ids\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    groups[grpIndex].grpsize = 1;
    groups[grpIndex].adminlen = 1;

    // sending joiing request to each existing client from list
    for (int i = 0; i < argcount; i++)
    {
        int fd = getClientFD(groups[grpIndex].tempMembers[i]);
        if (fd != -1)
        {
            bzero(message, 256);
            sprintf(message, "[%d] : Wanna join the group %d?\n", adminid, groups[grpIndex].groupid);
            send(fd, message, sizeof(message), 0);
            groups[grpIndex].reqSize++;
        }
        else
        {
            bzero(message, 256);
            sprintf(message, "Member with id %d does not exist\n", groups[grpIndex].tempMembers[i]);
            send(fd, message, sizeof(message), 0);
        }
    }
    // confirmation to admin client
    bzero(message, 256);
    sprintf(message, "**Request sent to all existing members for group %d**\n", groups[grpIndex].groupid);
    send(adminfd, message, sizeof(message), 0);
    grpIndex++;
}
// accept the joining request to group
void joinGroup(int grpid, int clientfd)
{
    int _grpindex = getGroupIndex(grpid);
    char message[256];
    if (_grpindex == -1)
    {
        bzero(message, 256);
        sprintf(message, "**Group does not exist!**\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    int clientid = getClientId(clientfd);

    if (isMember(_grpindex, clientid) == 1)
    {
        bzero(message, 256);
        sprintf(message, "**You are already in this group!**\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    if (isInvited(_grpindex, clientid) == 0)
    {
        bzero(message, 256);
        sprintf(message, "**You are not invited to this group!**\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    if (groups[_grpindex].grpsize == 5)
    {
        bzero(message, 256);
        sprintf(message, "**Group is full now!**\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    // pushing new member to members array in group at _grpindex
    groups[_grpindex].membersid[groups[_grpindex].grpsize] = clientid;
    bzero(message, 256);
    sprintf(message, "[Group %d] : You are added the group!\n", groups[_grpindex].groupid);
    send(clientfd, message, sizeof(message), 0);

    bzero(message, 256);
    sprintf(message, "[Group %d] : **%d accepted the request to join the group**\n", grpid, clientid);
    send(getClientFD(groups[_grpindex].admins[0]), message, sizeof(message), 0);
    // broadcasting message to all members
    bzero(message, 256);
    sprintf(message, "[Group %d] : %d is added the group!\n", groups[_grpindex].groupid, clientid);
    sendGroup(message, grpid, groups[_grpindex].admins[0]);
    // Insert group id in client object
    clientList[clientfd % 10]->joinedGroups[clientList[clientfd % 10]->grpCount++] = grpid;

    // decrease pending request count and increment group size
    groups[_grpindex].reqSize--;
    groups[_grpindex].grpsize++;

    // create group if all pending requests are processed
    if (groups[_grpindex].reqSize == 0)
    {
        groups[_grpindex].isCreated = true;
    }
}
// adjust pending request counts of group
void removeAndAdjustRequests(int _grpindex, int rmindex)
{
    // shifting array elements by one position from removal index
    for (int i = rmindex; i < 3; i++)
    {
        groups[_grpindex].tempMembers[i] = groups[_grpindex].tempMembers[i + 1];
    }
    groups[_grpindex].tempMembers[3] = 0;
    // decreasing request size
    groups[_grpindex].reqSize--;
}
// decline the request to join the group
void declineGroup(int grpid, int clientfd)
{
    int _grpindex = getGroupIndex(grpid);
    char message[256];
    if (_grpindex == -1)
    {
        bzero(message, 256);
        sprintf(message, "**Group does not exist!**\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    int clientid = getClientId(clientfd);

    if (isInvited(_grpindex, clientid) == 0)
    {
        bzero(message, 256);
        sprintf(message, "**You are not invited to this group!**\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    for (int i = 0; i < groups[_grpindex].reqSize; i++)
    {
        if (groups[_grpindex].tempMembers[i] == clientid)
        {
            // removing member and adjusting the member array
            removeAndAdjustRequests(_grpindex, i);
            bzero(message, 256);
            sprintf(message, "[Group %d] : **%d declined the request to join the group**\n", grpid, clientid);
            send(getClientFD(groups[_grpindex].admins[0]), message, sizeof(message), 0);
            if (groups[_grpindex].reqSize == 0)
            {
                groups[_grpindex].isCreated = true;
            }
            break;
        }
    }
}
// make a client admin of the group
void addAdmin(int grpid, int clientid, int adminid)
{
    printf("GRPID: %d CLIENTID: %d ADMINID: %d\n", grpid, clientid, adminid);
    int _grpindex = getGroupIndex(grpid);
    char message[256];

    // group does not exist
    if (_grpindex == -1)
    {
        bzero(message, 256);
        sprintf(message, "Group does not exist!\n");
        send(getClientFD(adminid), message, sizeof(message), 0);
        return;
    }
    if (groups[_grpindex].isCreated == false)
    {
        bzero(message, 256);
        sprintf(message, "The group is not created yet or deactivated\n");
        send(getClientFD(adminid), message, sizeof(message), 0);
        return;
    }
    // caller client is not an admin
    if (isAdmin(_grpindex, adminid) == 0)
    {
        bzero(message, 256);
        sprintf(message, "You are not an admin of this group!\n");
        send(getClientFD(adminid), message, sizeof(message), 0);
        return;
    }
    // client is not in the froup
    if (isMember(_grpindex, clientid) == 0)
    {
        bzero(message, 256);
        sprintf(message, "Client is not in this group!\n");
        send(getClientFD(adminid), message, sizeof(message), 0);
        return;
    }
    // clientid is already an admin
    if (isAdmin(_grpindex, clientid) == 1)
    {
        bzero(message, 256);
        sprintf(message, "Client is already an admin!\n");
        send(getClientFD(adminid), message, sizeof(message), 0);
        return;
    }

    groups[_grpindex].admins[groups[_grpindex].adminlen] = clientid;
    groups[_grpindex].adminlen++;
    bzero(message, 256);
    sprintf(message, "[Group %d] : You are made an admin of group by %d!\n", groups[_grpindex].groupid, adminid);
    send(getClientFD(clientid), message, sizeof(message), 0);
    // broadcasting new admin added message
    bzero(message, 256);
    sprintf(message, "%d is made an admin of group\n", clientid);
    sendGroup(message, grpid, getClientFD(clientid));
}
// add a new memeber to group
void addMember(char *request, int adminfd)
{
    int grpid;
    int clientArgs[3];
    char message[256];

    // splitting request
    int argCount = sscanf(request, "/addtogroup %d %d %d %d\n", &grpid, &clientArgs[0], &clientArgs[1], &clientArgs[2]);

    // no member id provided
    if (argCount == 1)
    {
        bzero(message, 256);
        sprintf(message, "Provide at least one member id\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    // getting groupindex
    int _grpindex = getGroupIndex(grpid);

    // group does not exist
    if (_grpindex == -1)
    {
        bzero(message, 256);
        sprintf(message, "Group does not exist!\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    // caller client is not an admin
    if (isAdmin(_grpindex, getClientId(adminfd)) == 0)
    {
        bzero(message, 256);
        sprintf(message, "You are not an admin of this group!\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    if (groups[_grpindex].isCreated == false)
    {
        bzero(message, 256);
        sprintf(message, "The group is not created yet! Waiting for everyone's response.\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    int i = 0;

    // inserting one by one into group
    while (--argCount)
    {
        // group is full
        if (groups[_grpindex].grpsize == 5)
        {
            bzero(message, 256);
            sprintf(message, "Group is already full! Can't add more member\n");
            send(adminfd, message, sizeof(message), 0);
            return;
        }

        // member does not exist in our records
        if (isClient(clientArgs[i]) == 0)
        {
            bzero(message, 256);
            sprintf(message, "%d does not exist\n", clientArgs[i++]);
            send(adminfd, message, sizeof(message), 0);
            continue;
        }

        // already in group
        if (isMember(_grpindex, clientArgs[i]) == 1)
        {
            bzero(message, 256);
            sprintf(message, "%d is already in the group\n", clientArgs[i++]);
            send(adminfd, message, sizeof(message), 0);
            continue;
        }

        // pushing new member to members array in group at _grpindex
        groups[_grpindex].membersid[groups[_grpindex].grpsize] = clientArgs[i];
        bzero(message, 256);
        sprintf(message, "[Group %d] : You are added to group!\n", groups[_grpindex].groupid);
        send(getClientFD(clientArgs[i]), message, sizeof(message), 0);
        // send(adminfd, message, sizeof(message), 0);

        int fd = getClientFD(clientArgs[i]);
        // Insert group id in client object
        clientList[fd % 10]->joinedGroups[(clientList[fd % 10]->grpCount)++] = grpid;

        // increase groupsize
        groups[_grpindex].grpsize++;

        // sending success message to all members
        bzero(message, 256);
        sprintf(message, "[Group %d] : %d is added to group!\n", groups[_grpindex].groupid, clientArgs[i]);
        sendGroup(message, grpid, clientArgs[i]);
        i++;
    }
}
// function to remove from admins
void removeFromAdmins(int _grpindex, int adminid)
{
    int rmindex;

    for (int i = 0; i < 5; i++)
    {
        if (adminid == groups[_grpindex].admins[i])
        {
            rmindex = i;
            break;
        }
    }

    for (int i = rmindex; i < 4; i++)
    {
        groups[_grpindex].admins[i] = groups[_grpindex].admins[i + 1];
    }
    groups[_grpindex].admins[4] = 0;
    groups[_grpindex].adminlen--;
}
// adjust indexes of members in group after removing a client
void removeAndAdjustGroupMembers(int _grpindex, int rmindex)
{
    // remove from admin also if he is an admin
    if (isAdmin(_grpindex, groups[_grpindex].membersid[rmindex]) == 1)
    {
        removeFromAdmins(_grpindex, groups[_grpindex].membersid[rmindex]);
    }

    // shifting array elements by one position from removal index
    for (int i = rmindex; i < 4; i++)
    {
        groups[_grpindex].membersid[i] = groups[_grpindex].membersid[i + 1];
    }
    groups[_grpindex].membersid[4] = 0;
    // decreasing group size
    groups[_grpindex].grpsize--;
}
// remove a member from group
void removeMember(char *request, int adminfd)
{
    int grpid;
    int clientArgs[4];
    char message[256];

    // splitting request
    int argCount = sscanf(request, "/removefromgroup %d %d %d %d %d\n", &grpid, &clientArgs[0], &clientArgs[1], &clientArgs[2], &clientArgs[3]);

    // no member id provided
    if (argCount == 1)
    {
        bzero(message, 256);
        sprintf(message, "Provide at least one member id\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    // getting groupindex
    int _grpindex = getGroupIndex(grpid);

    // group does not exist
    if (_grpindex == -1)
    {
        bzero(message, 256);
        sprintf(message, "Group does not exist!\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    // caller client is not an admin
    if (isAdmin(_grpindex, getClientId(adminfd)) == 0)
    {
        bzero(message, 256);
        sprintf(message, "You are not an admin of this group!\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }

    if (groups[_grpindex].isCreated == false)
    {
        bzero(message, 256);
        sprintf(message, "The group is not created yet! Waiting for everyone's response.\n");
        send(adminfd, message, sizeof(message), 0);
        return;
    }
    int j = 0;

    // inserting one by one into group
    while (--argCount)
    {
        // member does not exist in our records
        if (isClient(clientArgs[j]) == 0)
        {
            bzero(message, 256);
            sprintf(message, "%d does not exist\n", clientArgs[j++]);
            send(adminfd, message, sizeof(message), 0);
            continue;
        }

        for (int i = 0; i < 5; i++)
        {
            if (groups[_grpindex].membersid[i] == clientArgs[j])
            {
                // removing member and adjusting the member array
                removeAndAdjustGroupMembers(_grpindex, i);
                bzero(message, 256);
                sprintf(message, "[Group %d] : You are removed from the group\n", grpid);
                send(getClientFD(clientArgs[j]), message, sizeof(message), 0);
                bzero(message, 256);
                sprintf(message, "[Group %d] : %d is removed from the group\n", grpid, clientArgs[j]);
                sendGroup(message, grpid, getClientId(adminfd));
            }
        }
    }
}
// change the group to admin-only group
void makeGroupBroadcast(int grpid, int clientfd)
{
    int _grpindex = getGroupIndex(grpid);
    char message[256];
    // group does not exist
    if (_grpindex == -1)
    {
        bzero(message, 256);
        sprintf(message, "Group does not exist!\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }
    // caller client is not an admin
    if (isAdmin(_grpindex, getClientId(clientfd)) == 0)
    {
        bzero(message, 256);
        sprintf(message, "You are not an admin of this group!\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    if (groups[_grpindex].isCreated == false)
    {
        bzero(message, 256);
        sprintf(message, "The group is not created yet! Waiting for everyone's response.\n");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    groups[_grpindex].isBroadcast = true;
    sendGroup("**This group is now admin-only!**", grpid, clientfd);
}
// remove client from all groups and records
void removeClientFromAllGroups(int clientid)
{
    // fetch client fd and index
    int clientfd = getClientFD(clientid);
    int clientindex = clientfd % 10;
    char message[256];

    // get number of groups client has joined
    int _grpcount = clientList[clientindex]->grpCount;
    printf("Grp count: %d\n", _grpcount);

    for (int gindex = 0; gindex < _grpcount; gindex++)
    {
        // take up group one by one and remove this client
        int grpid = clientList[clientindex]->joinedGroups[gindex];
        int _grpindex = getGroupIndex(grpid);
        if (_grpindex == -1)
            continue;
        if (groups[_grpindex].isCreated == false)
            continue;
        for (int i = 0; i < 5; i++)
        {
            if (groups[_grpindex].membersid[i] == clientid)
            {
                // removing member and adjusting the member array
                removeAndAdjustGroupMembers(_grpindex, i);
                bzero(message, 256);
                sprintf(message, "**%d left the group %d.**", clientid, grpid);
                // notify other members about him
                sendGroup(message, grpid, clientfd);
                // if all are removed then close the group
                if (groups[_grpindex].grpsize == 0 || groups[_grpindex].adminlen == 0)
                {
                    groups[_grpindex].isCreated = false;
                    printf(">> All admins of group %d has left. Group has been deactivated!\n", groups[_grpindex].groupid);
                }
                break;
            }
        }
    }
}
// return all groups, a client is member of
void activeGroups(int clientfd)
{
    int _clientindex = clientfd % 10;
    char message[256];
    int grpcount = clientList[_clientindex]->grpCount;
    bool flag = false;

    if (grpcount == 0)
    {
        bzero(message, 256);
        sprintf(message, "No groups found!");
        send(clientfd, message, sizeof(message), 0);
        return;
    }

    for (int i = 0; i < grpcount; i++)
    {
        if (isActiveGroup(clientList[_clientindex]->joinedGroups[i]) == true)
        {
            flag = true;
            // getting group details
            int grpid = clientList[_clientindex]->joinedGroups[i];
            int _grpindex = getGroupIndex(grpid);

            // send group id
            bzero(message, 256);
            sprintf(message, "======= Group ID : %d ========", grpid);
            send(clientfd, message, sizeof(message), 0);

            // get members list
            char members[256];
            bzero(members, 256);
            char temp[8];
            bzero(message, 256);
            sprintf(message, "Members:");
            send(clientfd, message, sizeof(message), 0);
            for (int m = 0; m < groups[_grpindex].grpsize; m++)
            {
                bzero(temp, 8);
                sprintf(temp, " %d ", groups[_grpindex].membersid[m]);
                strcat(members, temp);
            }
            // send member list
            send(clientfd, members, sizeof(members), 0);
            // puts(members);

            // get admins list
            char admins[256];
            bzero(admins, 256);
            bzero(message, 256);
            sprintf(message, "Admins:");
            send(clientfd, message, sizeof(message), 0);
            for (int m = 0; m < groups[_grpindex].adminlen; m++)
            {
                bzero(temp, 8);
                sprintf(temp, " %d ", groups[_grpindex].admins[m]);
                strcat(admins, temp);
            }
            // send admin list
            send(clientfd, admins, sizeof(admins), 0);
            // puts(admins);
        }
    }
    if (flag == false)
    {
        bzero(message, 256);
        sprintf(message, "No active groups found!");
        send(clientfd, message, sizeof(message), 0);
    }
}
// send admin request from client to all admins
void adminRequest(int grpid, int clientid)
{
    int _grpindex = getGroupIndex(grpid);
    char message[256];
    // group does not exist
    if (_grpindex == -1)
    {
        bzero(message, 256);
        sprintf(message, "Group does not exist!\n");
        send(getClientFD(clientid), message, sizeof(message), 0);
        return;
    }
    if (groups[_grpindex].isCreated == false)
    {
        bzero(message, 256);
        sprintf(message, "The group is not created yet! Waiting for everyone's response.\n");
        send(getClientFD(clientid), message, sizeof(message), 0);
        return;
    }
    // client is not in the froup
    if (isMember(_grpindex, clientid) == 0)
    {
        bzero(message, 256);
        sprintf(message, "Client is not in this group!\n");
        send(getClientFD(clientid), message, sizeof(message), 0);
        return;
    }
    // clientid is already an admin
    if (isAdmin(_grpindex, clientid) == 1)
    {
        bzero(message, 256);
        sprintf(message, "Client is already an admin!\n");
        send(getClientFD(clientid), message, sizeof(message), 0);
        return;
    }
    // adding admin request in records to track it anytime
    adminRequests[admReqIndex].grpid = grpid;
    adminRequests[admReqIndex].memberid = clientid;
    adminRequests[admReqIndex].status = false;
    adminRequests[admReqIndex].posCount = 0;
    adminRequests[admReqIndex].negCount = 0;
    adminRequests[admReqIndex].totalAdmins = groups[_grpindex].adminlen;
    // notifying admins about admin request from a member
    for (int i = 0; i < groups[_grpindex].adminlen; i++)
    {
        bzero(message, 256);
        sprintf(message, "[Group %d] : %d wants to be an admin!\n", grpid, clientid);
        send(getClientFD(groups[_grpindex].admins[i]), message, sizeof(message), 0);
    }

    admReqIndex++;
}
int getAdminRequestIndex(int grpid, int clientid)
{
    for (int i = 0; i < admReqIndex; i++)
    {
        if (adminRequests[i].grpid == grpid && adminRequests[i].memberid == clientid)
            return i;
    }
    return -1;
}
// approve admin request of a client
void approveAdminReq(int grpid, int clientid, int adminid)
{
    // get adminrequest object from records
    int _reqindex = getAdminRequestIndex(grpid, clientid);
    char message[256];

    if (_reqindex == -1 || adminRequests[_reqindex].status == true)
    {
        bzero(message, 256);
        sprintf(message, "Either request is already processed or does not exist!");
        send(getClientFD(adminid), message, sizeof(message), 0);
        return;
    }

    adminRequests[_reqindex].posCount++;
    if (adminRequests[_reqindex].posCount + adminRequests[_reqindex].negCount == adminRequests[_reqindex].totalAdmins)
    {
        if (adminRequests[_reqindex].posCount >= adminRequests[_reqindex].negCount)
        {
            // add as admin
            addAdmin(grpid, clientid, adminid);
        }
        else
        {
            // send negative response to requesting client
            bzero(message, 256);
            sprintf(message, "Your request to join group %d has been declined by majority!", grpid);
            send(getClientFD(clientid), message, sizeof(message), 0);
        }
        // set req status as true
        adminRequests[_reqindex].status = true;
    }
}
// decline admin request of a client
void declineAdminReq(int grpid, int clientid, int adminid)
{
    // get adminrequest object from records
    int _reqindex = getAdminRequestIndex(grpid, clientid);
    char message[256];

    if (_reqindex == -1 || adminRequests[_reqindex].status == true)
    {
        bzero(message, 256);
        sprintf(message, "Either request is already processed or does not exist!");
        send(getClientFD(adminid), message, sizeof(message), 0);
        return;
    }

    adminRequests[_reqindex].negCount++;
    if (adminRequests[_reqindex].posCount + adminRequests[_reqindex].negCount == adminRequests[_reqindex].totalAdmins)
    {
        if (adminRequests[_reqindex].posCount >= adminRequests[_reqindex].negCount)
        {
            // add as admin
            addAdmin(grpid, clientid, adminid);
        }
        else
        {
            // send negative response to requesting client
            bzero(message, 256);
            sprintf(message, "Your request to join group %d has been declined by majority!", grpid);
            send(getClientFD(clientid), message, sizeof(message), 0);
        }
        // set req status as true
        adminRequests[_reqindex].status = true;
    }
}
// function to add new client in our records
int addRecClient(int newfd)
{
    // WRITE YOUR CODE HERE
    char message[512];
    struct client newclient;
    newclient.socketfd = newfd;
    newclient.id = generateRandomId();

    if (clientList[newfd % 10] != NULL)
    {
        sprintf(message, "Connection limit reached! Try again later.");
        send(newfd, message, sizeof(message), 0);
        sprintf(message, "500");
        send(newfd, message, sizeof(message), 0);
        logger(message);
        return -1;
    }

    clientList[newfd % 10] = malloc(sizeof(struct client));
    clientList[newfd % 10]->id = newclient.id;
    clientList[newfd % 10]->socketfd = newfd;
    clientList[newfd % 10]->grpCount = 0;
    clientList[newfd % 10]->abuseCount = 0;

    return newclient.id;
}
// function to remove client from our records
void removeRecClient(int clientfd)
{
    // WRITE YOUR CODE HERE
    char buf[256];
    int csock = getClientId(clientfd);
    for (int j = 0; j < 10; j++)
    {
        if (clientList[j] != NULL && clientList[j]->socketfd == clientfd)
        {
            removeClientFromAllGroups(clientList[j]->id);
            clientList[j] = NULL;
        }
        else if (clientList[j] != NULL)
        {
            // notifying other clients about removal
            bzero(buf, 256);
            sprintf(buf, "Client %d left the chat!", clientfd);
            send(clientList[j]->socketfd, buf, sizeof(buf), 0);
        }
    }
    bzero(buf, 256);
    sprintf(buf, "500");
    send(clientfd, buf, sizeof(buf), 0);
}
void completeRequest(int clientfd)
{
    char buf[128];
    bzero(buf, 128);
    sprintf(buf, "%d", 200);
    send(clientfd, buf, sizeof(buf), 0);
}
// handler for /active command
void printAllOnlineClients(int clientfd)
{
    // WRITE YOUR CODE HERE
    logger("/active from socket-%d\n", clientfd);
    char buf[256];
    for (int i = 0; i < 10; i++)
    {
        if (clientList[i] != NULL && clientList[i]->socketfd != clientfd)
        {
            bzero(buf, 256);
            sprintf(buf, "ID: %d Socket: %d", clientList[i]->id, clientList[i]->socketfd);
            send(clientfd, buf, sizeof(buf), 0);
        }
    }
}
// logger to log sent messages in file
void addMsgEntry(char *message, int destid, int clientfd)
{
    // WRITE YOUR CODE HERE
    int from = getClientId(clientfd);
    FILE *fptr;

    fptr = fopen("message_logs.txt", "a");
    char log_text[512];
    if (destid == -1)
        sprintf(log_text, "Broadcast From:%d Message:%s\n", from, message);
    else
        sprintf(log_text, "From:%d To:%d Message:%s\n", from, destid, message);
    fputs(log_text, fptr);
    fclose(fptr);
}
/* function to remove an entry from Shared Memory Segment for storing list of messages from clients*/
void removeMsgEntry()
{
    // WRITE YOUR CODE HERE
    printf("REMOVE MSG ENTRY\n");
}
/* function to processs messages from clients*/
int sendMsg(char *message, int destid, int clientfd)
{
    // WRITE YOUR CODE HERE
    int sender = getClientId(clientfd);

    pid_t pid = 0;
    int status;
    char *arglist[] = {"python3", "exam.py", message, NULL};
    pid = fork();
    if (pid == 0)
    {
        // printf("I am the child.\\n");
        execvp("python3", arglist);
        perror("In exec(): ");
    }
    if (pid > 0)
    {
        // printf("I am the parent, and the child is %d.\\n", pid);
        pid = wait(&status);
        FILE *fptr;

        fptr = fopen("res.txt", "r");
        char line[100]; // buffer to hold each line
        fgets(line, sizeof(line), fptr);
        puts(line);

        if (strncmp(line, "hate_abusive", 12) == 0)
        {
            char buf[512];
            bzero(buf, 512);
            sprintf(buf, "Sent abusive message. !!Msg  locked!!");
            send(clientfd, buf, sizeof(buf), 0);
            clientList[clientfd % 10]->abuseCount++;
            if (clientList[clientfd % 10]->abuseCount >= 5)
            {
                removeRecClient(clientfd);
            }
            return 2;
        }
        // printf("End of process %d: ", pid);
        if (WIFEXITED(status))
        {
            printf("The process ended with exit(%d).\\n", WEXITSTATUS(status));
        }
        if (WIFSIGNALED(status))
        {
            printf("The process ended with kill -%d.\\n", WTERMSIG(status));
        }
    }
    if (pid < 0)
    {
        perror("In fork():");
    }

    for (int i = 0; i < 10; i++)
    {
        if (clientList[i] != NULL && clientList[i]->id == destid)
        {
            char buf[512];
            bzero(buf, 512);
            sprintf(buf, "%d:/ %s", sender, message);
            send(clientList[i]->socketfd, buf, sizeof(buf), 0);
            // completeRequest(clientList[i]->socketfd);
            return 1;
        }
    }
    return -1;
}
/*FUNCTION TO HANDLE BROADCAST REQUEST*/
void broadcast(char *message, int clientfd)
{
    // WRITE YOUR CODE HERE
    int sender = getClientId(clientfd);
    char buf[512];

    pid_t pid = 0;
    int status;
    char *arglist[] = {"python3", "exam.py", message, NULL};
    pid = fork();
    if (pid == 0)
    {
        // printf("I am the child.\\n");
        execvp("python3", arglist);
        perror("In exec(): ");
    }
    if (pid > 0)
    {
        // printf("I am the parent, and the child is %d.\\n", pid);
        pid = wait(&status);
        FILE *fptr;

        fptr = fopen("res.txt", "r");
        char line[100]; // buffer to hold each line
        fgets(line, sizeof(line), fptr);
        puts(line);

        if (strncmp(line, "hate_abusive", 12) == 0)
        {
            char buf[512];
            bzero(buf, 512);
            sprintf(buf, "Sent abusive message. !!Msg  locked!!");
            send(clientfd, buf, sizeof(buf), 0);
            printf("Message hasn't been sent to client because of abusiveness!!\n");
            clientList[clientfd % 10]->abuseCount++;
            if (clientList[clientfd % 10]->abuseCount >= 5)
            {
                removeRecClient(clientfd);
            }
            return;
        }
        // printf("End of process %d: ", pid);
        if (WIFEXITED(status))
        {
            printf("The process ended with exit(%d).\\n", WEXITSTATUS(status));
        }
        if (WIFSIGNALED(status))
        {
            printf("The process ended with kill -%d.\\n", WTERMSIG(status));
        }
    }
    if (pid < 0)
    {
        perror("In fork():");
    }

    for (int i = 0; i < 10; i++)
    {
        if (clientList[i] != NULL && clientList[i]->socketfd != clientfd)
        {
            bzero(buf, 512);
            sprintf(buf, "%d:/ %s", sender, message);
            send(clientList[i]->socketfd, buf, sizeof(buf), 0);
        }
    }
}
/*Function to handle all the commands as entered by the client*/
int performAction(char *request, int clientfd)
{
    char buf[256];
    if (strncmp(request, "/activegroups", 13) == 0)
    {
        activeGroups(clientfd);
    }
    else if (strncmp(request, "/active", 7) == 0)
    {
        // printf("/active request arrived from %d\n", clientfd);
        printAllOnlineClients(clientfd);
    }
    else if (strncmp(request, "/send ", 6) == 0)
    {
        // printf("/send request arrived from %d\n", clientfd);
        // puts(request);

        char message[512];
        int destid;

        int count = sscanf(request, "/send %d %[^\n]\n", &destid, message);
        if (count != 2)
        {
            bzero(buf, 256);
            sprintf(buf, "Please provide destination id and message! [/send ID MSG]");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            // puts(message);
            // printf("Dest id: %d\n", destid);
            logger("/send from %d to %d => %s\n", clientfd, destid, message);
            int status = sendMsg(message, destid, clientfd);

            if (status == 1)
            {
                addMsgEntry(message, destid, clientfd);
                logger("message sent to %d\n", destid);
            }
            else if (status == 2)
            {
                printf("Message hasn't been sent to client because of abusiveness!!\n");
            }
            else
            {
                bzero(buf, 256);
                sprintf(buf, "Client is offline, can't send the message.");
                send(clientfd, buf, sizeof(buf), 0);
                logger("%d is offline\n", destid);
            }
        }
    }
    else if (strncmp(request, "/broadcast", 10) == 0)
    {
        char message[512];

        int status = sscanf(request, "/broadcast %[^\n]\n", message);
        if (status != 1)
        {
            bzero(buf, 256);
            sprintf(buf, "Please enter a message!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            // puts(message);

            addMsgEntry(message, -1, clientfd);
            logger("/broadcast from %d => %s\n", clientfd, message);
            broadcast(message, clientfd);
        }
    }
    else if (strncmp(request, "/quit", 5) == 0)
    {
        removeRecClient(clientfd);
        return 0;
    }
    else if (strncmp(request, "/makegroupbroadcast", 19) == 0)
    {
        int grpid;
        if (sscanf(request, "/makegroupbroadcast %d\n", &grpid) < 1)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/makegroupbroadcast GID]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            makeGroupBroadcast(grpid, clientfd);
        }
    }
    else if (strncmp(request, "/makegroupreq", 13) == 0)
    {
        makeGroupReq(request, clientfd);
    }
    else if (strncmp(request, "/makegroup", 10) == 0)
    {
        makeGroup(request, clientfd);
    }
    else if (strncmp(request, "/makeadminreq", 13) == 0)
    {
        int grpid;
        if (sscanf(request, "/makeadminreq %d\n", &grpid) < 1)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/makeadminreq GRP_ID]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            adminRequest(grpid, getClientId(clientfd));
        }
    }
    else if (strncmp(request, "/makeadmin", 10) == 0)
    {
        int grpid, clientid, adminid;
        if (sscanf(request, "/makeadmin %d %d\n", &grpid, &clientid) < 2)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/makeadmin GRP_ID CLIENT_ID]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            addAdmin(grpid, clientid, getClientId(clientfd));
        }
    }
    else if (strncmp(request, "/addtogroup", 11) == 0)
    {
        addMember(request, clientfd);
    }
    else if (strncmp(request, "/removefromgroup", 16) == 0)
    {
        removeMember(request, clientfd);
    }
    else if (strncmp(request, "/sendgroup", 10) == 0)
    {
        int groupid;
        char message[256];
        if (sscanf(request, "/sendgroup %d %[^\n]\n", &groupid, message) < 2)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/sendgroup GID MESSAGE]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            sendGroup(message, groupid, clientfd);
        }
    }
    else if (strncmp(request, "/joingroup", 10) == 0)
    {
        int grpid;
        if (sscanf(request, "/joingroup %d\n", &grpid) < 1)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/joingroup GID]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            joinGroup(grpid, clientfd);
        }
    }
    else if (strncmp(request, "/declinegroup", 13) == 0)
    {
        int grpid;
        if (sscanf(request, "/declinegroup %d\n", &grpid) < 1)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/declinegroup GID]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            declineGroup(grpid, clientfd);
        }
    }
    else if (strncmp(request, "/approveadminreq", 15) == 0)
    {
        int grpid, clientid;
        if (sscanf(request, "/approveadminreq %d %d\n", &grpid, &clientid) < 2)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/approveadminreq GRP_ID CLIENT_ID]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            approveAdminReq(grpid, clientid, getClientId(clientfd));
        }
    }
    else if (strncmp(request, "/declineadminreq", 15) == 0)
    {
        int grpid, clientid;
        if (sscanf(request, "/declineadminreq %d %d\n", &grpid, &clientid) < 2)
        {
            bzero(buf, 256);
            sprintf(buf, "Provide in valid format [/declineadminreq GRP_ID CLIENT_ID]!");
            send(clientfd, buf, sizeof(buf), 0);
        }
        else
        {
            declineAdminReq(grpid, clientid, getClientId(clientfd));
        }
    }
    else
    {
        bzero(buf, 256);
        sprintf(buf, "Request not supported!");
        send(clientfd, buf, sizeof(buf), 0);
        logger("Unsupported request from %d\n", clientfd);
    }
    return 1;
}
// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET)
    {
        return &(((struct sockaddr_in *)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6 *)sa)->sin6_addr);
}

int main(int argc, char *argv[])
{
    // signal(SIGINT, sigChandler);
    // signal(SIGSTOP, sigZhandler);
    // master stores all the socket descriptors that are currently connected, as well as the socket descriptor that is listening for new connections.
    fd_set master; // master file descriptor list

    fd_set read_fds; // temp file descriptor list for select()
    int fdmax;       // maximum file descriptor number

    int listener; // listening socket descriptor
    int newfd;    // newly accept()ed socket descriptor

    // make list null
    for (int i = 0; i < 10; i++)
    {
        clientList[i] = NULL;
    }

    struct sockaddr_storage remoteaddr; // client address
    socklen_t addrlen;

    char buf[256]; // buffer for client data
    int nbytes;

    char remoteIP[INET6_ADDRSTRLEN];

    int yes = 1; // for setsockopt() SO_REUSEADDR, below
    int i, j, rv;

    struct addrinfo hints, *ai, *p;

    FD_ZERO(&master); // clear the master and temp sets
    FD_ZERO(&read_fds);

    // get us a socket and bind it
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;
    //    allocates and initializes a linked
    //    list of addrinfo structures, one for each network address that
    //    matches node and service, subject to any restrictions imposed by
    //    hints, and returns a pointer to the start of the list in "ai".
    //    The items in the linked list are linked by the ai_next field.
    if ((rv = getaddrinfo(NULL, (argv[1]), &hints, &ai)) != 0)
    {
        fprintf(stderr, "server: %s\n", gai_strerror(rv));
        exit(1);
    }
    // loop checks for all service provider addresses and finds a free socket from it
    for (p = ai; p != NULL; p = p->ai_next)
    {
        // listener socket fd
        listener = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (listener < 0)
        {
            continue;
        }

        // Allows other sockets to bind() to this port, unless there is an active
        // listening socket bound to the port already. This enables you to get around
        // those “Address already in use” error messages when you try to restart your
        // server after a crash.
        setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));

        // bind the listener
        if (bind(listener, p->ai_addr, p->ai_addrlen) < 0)
        {
            close(listener);
            continue;
        }

        break;
    }
    // if we got here, it means we didn't get bound
    if (p == NULL)
    {
        fprintf(stderr, "server: failed to bind\n");
        exit(2);
    }
    freeaddrinfo(ai); // all done with this
    // listen
    if (listen(listener, 10) == -1)
    {
        perror("listen");
        exit(3);
    }
    // add the listener to the master set
    FD_SET(listener, &master);
    // keep track of the biggest file descriptor
    fdmax = listener; // so far, it's this one
    // main loop
    for (;;)
    {
        read_fds = master; // copy it because select() will modify it (we need to maintain all records in master)
        if (select(fdmax + 1, &read_fds, NULL, NULL, NULL) == -1)
        {
            perror("select");
            exit(4);
        }
        // if no error then read_fds will contain the fds of sockets which are ready for reading
        // run through the existing connections (till fdmax because that will be latest socket number which got connected) looking for data to read
        for (i = 0; i <= fdmax; i++)
        {
            //// i stores the socketfd of connected client or listener ////
            // check if the fd is ready for reeading in read_fds
            if (FD_ISSET(i, &read_fds))
            { // we got one!!
                if (i == listener)
                {
                    // this is our listener fd
                    // handle new connections
                    addrlen = sizeof remoteaddr;
                    newfd = accept(listener,
                                   (struct sockaddr *)&remoteaddr,
                                   &addrlen);

                    if (newfd == -1)
                        perror("accept");
                    else
                    {
                        char message[256];
                        FD_SET(newfd, &master); // add to master set

                        if (newfd > fdmax)
                        { // keep track of the max
                            fdmax = newfd;
                        }

                        int id = addRecClient(newfd);

                        if (id == -1)
                        {
                            close(newfd);           // bye!
                            FD_CLR(newfd, &master); // remove from master set
                            logger("Client limit reached!\n");
                            continue;
                        }

                        printf("server: new connection from %s on "
                               "socket %d with id %d\n",
                               inet_ntop(remoteaddr.ss_family,
                                         get_in_addr((struct sockaddr *)&remoteaddr),
                                         remoteIP, INET6_ADDRSTRLEN),
                               newfd, id);

                        sprintf(message, "Welcome! You are connected with ID:%d server:%d", id, listener);
                        send(newfd, message, sizeof(message), 0);
                    }
                }
                else
                {
                    // handle data from a client
                    bzero(buf, 256);
                    if ((nbytes = recv(i, buf, sizeof(buf), 0)) <= 0)
                    {
                        // got error or connection closed by client
                        if (nbytes <= 0)
                        {
                            int status = performAction("/quit", i);

                            if (status == 0)
                            {
                                logger("socket %d hung up\n", i);
                                close(i);           // close the client socket
                                FD_CLR(i, &master); // remove fd from master entry
                            }
                        }
                        else
                            perror("recv");
                    }
                    else
                    {
                        // we got some data from a client
                        int status = performAction(buf, i);
                        if (status == 0)
                        {
                            logger("socket %d hung up\n", i);
                            close(i);           // close the client socket
                            FD_CLR(i, &master); // remove fd from master entry
                        }
                    }
                } // END handle data from client
            }     // END got new incoming connection
        }         // END looping through file descriptors
    }             // END for(;;)--and you thought it would never end!
    return 0;
}