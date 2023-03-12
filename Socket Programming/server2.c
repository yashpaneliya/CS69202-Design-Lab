#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <ctype.h>
#include <stdbool.h>

/////////////////////////////////////////////////////////////////////////
//                             ID: 22CS60R70                           //
//                              SERVER CODE                            //
//      How to run?                                                    //
//      - gcc server2.c -o server                                      //
//      - ./server                                                     //
//                                                                     //
/////////////////////////////////////////////////////////////////////////

// data file name
char *FILENAME = "student_info.txt";

// structure to store student data
struct Student
{
    int id;
    char name[50];
    int marks[5];
};

// function to swap element of array
void swap(struct Student *A, struct Student *B)
{
    struct Student temp = *A;
    *A = *B;
    *B = temp;
}

// structure to store rank data of a student
struct Rank
{
    int rollnum;
    char name[50];
    double avg;
    int rank;
};

// function to swap element of array
void swapRank(struct Rank *A, struct Rank *B)
{
    struct Rank temp = *A;
    *A = *B;
    *B = temp;
}

void error(char *msg)
{
    perror(msg);
    exit(0);
}

// calculate grade according to marks
char *returnGrade(double mark)
{
    char *grade;
    if (mark >= 90)
    {
        grade = "EX";
    }
    else if (mark >= 80)
    {
        grade = "A";
    }
    else if (mark >= 70)
    {
        grade = "B";
    }
    else if (mark >= 60)
    {
        grade = "C";
    }
    else if (mark >= 50)
    {
        grade = "D";
    }
    else if (mark >= 40)
    {
        grade = "P";
    }
    else
    {
        grade = "F";
    }
    return grade;
}

// function to sort file data
// newsockfd: socket id
void handleSortX(int newsockfd, char *query)
{
    // variable to store parameters
    int start = 0, end = __INT_MAX__;
    char field[5];
    char q[50];

    // splitting the params from query
    char *token = strtok(query, " ");
    token = strtok(NULL, " ");
    if (token != NULL)
    {
        strcpy(field, token);
        token = strtok(NULL, " ");
        if (token != NULL)
        {
            start = atoi(token);
            // error checking
            if (start < 0)
            {
                char buffer[50];
                sprintf(buffer, "%s", "Invalid input\n");
                write(newsockfd, buffer, sizeof(buffer));
                return;
            }

            if (start != 0)
                start--;

            token = strtok(NULL, "\n");
            if (token != NULL)
            {
                end = atoi(token) - 1;
                // error checking
                if (end < 0)
                {
                    char buffer[50];
                    sprintf(buffer, "%s", "Invalid input\n");
                    write(newsockfd, buffer, sizeof(buffer));
                    return;
                }
            }
        }
    }

    // puts(field);
    // printf("Start: %d End:%d\n", start, end);

    FILE *fp;

    // Opening file in read mode
    fp = fopen(FILENAME, "r");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return;
    }

    char buffer[512];
    bzero(buffer, 512);

    // array to store students data
    struct Student students[256];

    // index to track current student data
    int i = 0;
    // total number of rows in the given range
    int count = 0;

    char line[100]; // buffer to hold each line
    while (fgets(line, sizeof(line), fp))
    { // read one line at a time
        if (i < start)
        {
            ++i;
            continue;
        }
        if (i > end)
            break;
        // temporary variables to store splitted line
        // to store roll number
        int id;
        // to store name
        char name[50];
        // to store marks for calculating sum and average
        int grades[5];
        // extracting the variables from scanned line from file
        if (sscanf(line, "%d\t%[^\t]\t%d\t%d\t%d\t%d\t%d", &id, name, &grades[0], &grades[1], &grades[2], &grades[3], &grades[4]) != 7)
        {
            continue;
        }
        // appending current data to array
        students[i - start].id = id;
        sprintf(students[i - start].name, "%s", name);
        students[i - start].marks[0] = grades[0];
        students[i - start].marks[1] = grades[1];
        students[i - start].marks[2] = grades[2];
        students[i - start].marks[3] = grades[3];
        students[i - start].marks[4] = grades[4];
        ++i;
        ++count;
        bzero(name, 50);
    }

    end = count;

    int j;
    // sorting logic
    for (i = 0; i < count - 1; i++)
    {
        for (j = 0; j < count - i - 1; j++)
        {
            // comparing the values according to fields
            // swapping respective elements
            if (strncmp("R", field, 1) == 0)
            {
                if (students[j].id > students[j + 1].id)
                {
                    swap(&students[j], &students[j + 1]);
                }
            }
            else if (strncmp("S", field, 1) == 0)
            {
                if (strcmp(students[j].name, students[j + 1].name) > 0)
                {
                    swap(&students[j], &students[j + 1]);
                }
            }
            else if (strncmp("A_1", field, 3) == 0)
            {
                if (students[j].marks[0] > students[j + 1].marks[0])
                {
                    swap(&students[j], &students[j + 1]);
                }
            }
            else if (strncmp("A_2", field, 3) == 0)
            {
                if (students[j].marks[1] > students[j + 1].marks[1])
                {
                    swap(&students[j], &students[j + 1]);
                }
            }
            else if (strncmp("A_3", field, 3) == 0)
            {
                if (students[j].marks[2] > students[j + 1].marks[2])
                {
                    swap(&students[j], &students[j + 1]);
                }
            }
            else if (strncmp("A_4", field, 3) == 0)
            {
                if (students[j].marks[3] > students[j + 1].marks[3])
                {
                    swap(&students[j], &students[j + 1]);
                }
            }
            else if (strncmp("A_5", field, 3) == 0)
            {
                if (students[j].marks[4] > students[j + 1].marks[4])
                {
                    swap(&students[j], &students[j + 1]);
                }
            }
            else
            {
                bzero(buffer, 256);
                sprintf(buffer, "%s", "Invalid field to sort!");
                int n = write(newsockfd, buffer, sizeof(buffer));
                return;
            }
        }
    }

    // sending sorted data to client
    for (int i = 0; i < count; i++)
    {
        bzero(buffer, 256);
        sprintf(buffer, "%d %s %d %d %d %d %d", students[i].id, students[i].name, students[i].marks[0], students[i].marks[1], students[i].marks[2], students[i].marks[3], students[i].marks[4]);
        // sending calculated grade and student details to client one by one
        int n = write(newsockfd, buffer, sizeof(buffer));
    }
}

// function to generate rank of the student
// rollnum: roll number of student whose rank is to be generated
void handleRankX(int rollnum, int newsockfd)
{
    FILE *fp;

    // Opening file in read mode
    fp = fopen(FILENAME, "r");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return;
    }

    char buffer[512];
    bzero(buffer, 512);

    struct Rank ranks[250];
    int i = 0;
    int count = 0;

    char line[100]; // buffer to hold each line
    while (fgets(line, sizeof(line), fp))
    { // read one line at a time
        // temporary variables to store splitted line
        // to store roll number
        int id;
        // to store name
        char name[50];
        // to store marks for calculating sum and average
        int grades[5];
        // extracting the variables from scanned line from file
        if (sscanf(line, "%d\t%[^\t]\t%d\t%d\t%d\t%d\t%d", &id, name, &grades[0], &grades[1], &grades[2], &grades[3], &grades[4]) != 7)
        {
            continue;
        }
        // appending current data to array
        ranks[i].rollnum = id;
        // calculating average marks
        ranks[i].avg = (grades[0] + grades[1] + grades[2] + grades[3] + grades[4]) / 5.0;
        ranks[i].rank = 0;
        sprintf(ranks[i].name, "%s", name);
        ++i;
        ++count;
        bzero(name, 50);
    }

    int j;
    // sorting according to average marks
    for (i = 0; i < count - 1; i++)
    {
        for (j = 0; j < count - i - 1; j++)
        {
            if (ranks[j].avg < ranks[j + 1].avg)
                swapRank(&ranks[j], &ranks[j + 1]);
        }
    }

    // printing top 10 students
    if (rollnum == -1)
    {
        for (i = 0; i < 10; i++)
        {
            bzero(buffer, 256);
            sprintf(buffer, "Roll num: %d Name: %s Rank:%d Avg: %f", ranks[i].rollnum, ranks[i].name, i + 1, ranks[i].avg);
            // sending student details with rank
            int n = write(newsockfd, buffer, sizeof(buffer));
        }
        return;
    }

    // assigning ranks in sorted array
    for (i = 0; i < count; i++)
    {
        if (rollnum == ranks[i].rollnum)
        {
            bzero(buffer, 256);
            sprintf(buffer, "Roll num: %d Name: %s Rank:%d Avg: %f", rollnum, ranks[i].name, i + 1, ranks[i].avg);
            // sending student details with rank
            int n = write(newsockfd, buffer, sizeof(buffer));
            return;
        }
    }

    bzero(buffer, 256);
    sprintf(buffer, "%s", "Roll number not found!");
    int n = write(newsockfd, buffer, sizeof(buffer));
    return;
}

void handleSimilarX(int newsockfd, int anum)
{
    // to store output string
    char buffer[512];
    bzero(buffer, 512);

    // checking valid assignment number
    if(anum<=0 || anum>=6)
    {
        bzero(buffer, 256);
        sprintf(buffer, "%s", "Please provide valid assignment number!");
        int n = write(newsockfd, buffer, sizeof(buffer));
        return;
    }
    FILE *fp;

    // Opening file in read mode
    fp = fopen(FILENAME, "r");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return;
    }

    struct Student students[256];

    int i = 0, count = 0;

    char line[100]; // buffer to hold each line
    while (fgets(line, sizeof(line), fp))
    {
        // temporary variables to store splitted line
        // to store roll number
        int id;
        // to store name
        char name[50];
        // to store marks for calculating sum and average
        int grades[5];
        // extracting the variables from scanned line from file
        if (sscanf(line, "%d\t%[^\t]\t%d\t%d\t%d\t%d\t%d\n", &id, name, &grades[0], &grades[1], &grades[2], &grades[3], &grades[4]) != 7)
        {
            continue;
        }

        // appending current data to array
        students[i].id = id;
        sprintf(students[i].name, "%s", name);
        students[i].marks[0] = grades[0];
        students[i].marks[1] = grades[1];
        students[i].marks[2] = grades[2];
        students[i].marks[3] = grades[3];
        students[i].marks[4] = grades[4];
        ++i;
        ++count;
        bzero(name, 50);
    }

    // sorting according to provides assignment number's marks
    for (i = 0; i < count - 1; i++)
    {
        for (int j = 0; j < count - i - 1; j++)
        {
            // comparing the values according to fields
            // swapping respective elements
            if (students[j].marks[anum-1] > students[j + 1].marks[anum-1])
            {
                swap(&students[j], &students[j + 1]);
            }
        }
    }

    int found = 0; // to ensure first entry only grts printed once in loop
    bool flag=false; // to check whether there exists any similar marks or not
    for (int i = 0; i < count; i++) {
        for (int j = i+1; j < count; j++) {
            // comparng marks of desired assignment
            if (students[i].marks[anum-1] == students[j].marks[anum-1]) {
                if(found==0)
                {
                    bzero(buffer, 256);
                    sprintf(buffer, "%d\t%s\t%d", students[i].id, students[i].name, students[i].marks[anum-1]);
                    int n = write(newsockfd, buffer, sizeof(buffer));
                }
                // skipping record in outer loop
                i++;
                bzero(buffer, 256);
                sprintf(buffer, "%d\t%s\t%d", students[j].id, students[j].name, students[j].marks[anum-1]);
                // sending student details
                int n = write(newsockfd, buffer, sizeof(buffer));
                found = 1;
                flag=true;
            }
        }
        found=0;
    }

    if (flag == false)
    {
        bzero(buffer, 256);
        sprintf(buffer, "%s", "No similar marks found!");
        int n = write(newsockfd, buffer, sizeof(buffer));
    }
}

// function to calculate grade of a student
// formatted_string: string to store output
// roll: student's roll number
void handleGradeX(char *formatted_string, int roll)
{
    FILE *fp;
    // Opening file in append mode
    fp = fopen(FILENAME, "r");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return;
    }

    char buffer[512];
    bzero(buffer, 512);

    // to store total of marks
    double sum = 0;

    bool flag = false;

    // temporary variables to store splitted line
    // to store roll number
    int id;
    // to store name
    char name[50];
    // to store marks for calculating sum and average
    int grades[5];

    char line[100]; // buffer to hold each line
    while (fgets(line, sizeof(line), fp))
    { // read one line at a time

        // extracting the variables from scanned line from file
        if (sscanf(line, "%d\t%[^\t]\t%d\t%d\t%d\t%d\t%d", &id, name, &grades[0], &grades[1], &grades[2], &grades[3], &grades[4]) != 7)
        {
            continue;
        }

        // sum the marks if roll number matches
        if (id == roll)
        {
            flag = true;
            sum = grades[0] + grades[1] + grades[2] + grades[3] + grades[4];
            break;
        }
    }

    // return message if roll number not found
    if (flag == false)
    {
        sprintf(formatted_string, "%s", "Roll number not found!\n");
    }
    else
    {
        // calculating average
        sum = sum / 5.0;
        sprintf(formatted_string, "%d %s %d %d %d %d %d %s", id, name, grades[0], grades[1], grades[2], grades[3], grades[4], returnGrade(sum));
    }
}

// function to return grades of all students
// newsockfd: current socket id
void handleGradeXAll(int newsockfd)
{
    FILE *fp;

    // Opening file in read mode
    fp = fopen(FILENAME, "r");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return;
    }

    // to store output string
    char buffer[512];
    bzero(buffer, 512);

    // to store sum of marks of individual student temporary
    double sum = 0;

    char line[100]; // buffer to hold each line
    while (fgets(line, sizeof(line), fp))
    { // read one line at a time
        // temporary variables to store splitted line
        // to store roll number
        int id;
        // to store name
        char name[50];
        // to store marks for calculating sum and average
        int grades[5];
        // extracting the variables from scanned line from file
        if (sscanf(line, "%d\t%[^\t]\t%d\t%d\t%d\t%d\t%d", &id, name, &grades[0], &grades[1], &grades[2], &grades[3], &grades[4]) != 7)
        {
            continue;
        }
        // calculating average
        sum = grades[0] + grades[1] + grades[2] + grades[3] + grades[4];
        sum = sum / 5.0;
        // sprintf(buffer, "%d %s %c\n", id, name, returnGrade(sum));
        sprintf(buffer, "%d %s %d %d %d %d %d %s", id, name, grades[0], grades[1], grades[2], grades[3], grades[4], returnGrade(sum));
        // sending calculated grade and student details to client one by one
        int n = write(newsockfd, buffer, sizeof(buffer));
    }
}

// function to calculate average of assignment
// index: assignment number
double handleAverage(int index)
{
    // error checking for assignment index out of bound
    if (index > 5 || index <= 0)
    {
        return -1.0;
    }
    FILE *fp;

    // Opening file in append mode
    fp = fopen(FILENAME, "r");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return 0;
    }

    char buffer[512];
    bzero(buffer, 512);

    int sum = 0;   // storing sum of all marks
    int count = 0; // counting number of entries

    char line[100]; // buffer to hold each line
    while (fgets(line, sizeof(line), fp))
    { // read one line at a time
        // to store roll number
        int id;
        // to store name
        char name[50];
        // to store marks for calculating sum and average
        int grades[5];

        // extracting the variables from scanned line from file
        if (sscanf(line, "%d\t%[^\t]\t%d\t%d\t%d\t%d\t%d", &id, name, &grades[0], &grades[1], &grades[2], &grades[3], &grades[4]) != 7)
        {
            grades[4] = 0;
        }

        sum += grades[index - 1];
        count++;
    }
    // returning average
    double average = (double)sum / count;
    return average;
}

// function to insert message in the file
// message: string to append on file
int handleInsert(char *message)
{
    // Open the file in append mode
    FILE *fp = fopen(FILENAME, "a");
    if (fp == NULL)
    {
        printf("File '%s' cannot be opened\n", FILENAME);
        return 0;
    }

    // check message format
    // to store roll number
    int id;
    // to store name
    char name[50];
    // to store marks for calculating sum and average
    int grades[5];

    // extracting the variables from scanned line from file
    if (sscanf(message, "%d\t%[^\t]\t%d\t%d\t%d\t%d\t%d", &id, name, &grades[0], &grades[1], &grades[2], &grades[3], &grades[4]) != 7)
    {
        return -1;
    }

    // check range of marks
    for (int i = 0; i < 5; ++i)
    {
        if (grades[i] < 0 || grades[i] > 100)
            return -1;
    }

    // Write the message to the file
    int status = fprintf(fp, "%s\n", message);

    // Close the file
    fclose(fp);

    return status;
}

// function to get number of rows in file
int handleNumrow()
{
    FILE *fp;
    char c;
    int count = 0;

    // Opening file in reading mode
    fp = fopen(FILENAME, "r");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return 0;
    }

    // counting lines
    char line[512];
    while (fgets(line, sizeof(line), fp))
    {
        ++count;
    }
    // printf("Total number of rows: %d\n",count);
    return count;
}

int main(int argc, char *argv[])
{
    int portno = 5000;
    struct sockaddr_in serv_addr;
    bzero((char *)&serv_addr, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);

    int sockfd;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        error("ERROR on binding\n");
    }

    listen(sockfd, 5);

    struct sockaddr_in cli_addr;
    socklen_t clilen;
    clilen = sizeof(cli_addr);

    int newsockfd;
    newsockfd = accept(sockfd, (struct sockaddr *)&cli_addr, &clilen);

    char buffer[256];
    int n;

    FILE *fp;

    // Opening file in append mode
    fp = fopen(FILENAME, "a");

    if (NULL == fp)
    {
        printf("File can't be opened \n");
        return 0;
    }

    fputs("\n", fp);
    fclose(fp);

    while (1)
    {
        bzero(buffer, 256);
        n = read(newsockfd, buffer, sizeof(buffer));

        if (n <= 0)
        {
            continue;
        }

        printf("Query: %s", buffer);
        char *query;
        strcpy(query, buffer);

        char *token = NULL;
        token = strtok(buffer, " ");

        if ((strcmp(buffer, "NUMROW\n")) == 0)
        {
            // handleRow() to count number of lines in file
            int count = handleNumrow();
            // flushing the buffer
            bzero(buffer, 256);
            // Storing output in buffer
            sprintf(buffer, "%d", count);
            // Sending response
            n = write(newsockfd, buffer, sizeof(buffer));
        }
        else if ((strcmp(token, "INSERT")) == 0)
        {
            // token: contains the message to insert
            token = strtok(NULL, "\n");
            // check whether message is there or not
            if (token == NULL)
            {
                // send error response
                sprintf(buffer, "%s", "Please provide input in valid format!\n");
                n = write(newsockfd, buffer, sizeof(buffer));
                bzero(buffer, 256);
                // continue;
            }
            // handleInsert() to insert the message
            int status = handleInsert(token);
            // flush out buffer
            bzero(buffer, 64);
            // check file write status and send response
            if (status < 0)
            {
                sprintf(buffer, "%s", "Failed to insert message! Check the format of message!\n");
            }
            else
            {
                sprintf(buffer, "%s", "Inserted successfully!\n");
            }
            n = write(newsockfd, buffer, sizeof(buffer));
        }
        else if ((strcmp(token, "AVERAGE")) == 0)
        {
            token = strtok(NULL, "\n");
            // check whether message is there or not
            if (token == NULL)
            {
                // send error response
                sprintf(buffer, "%s", "Please provide input in valid format!\n");
                n = write(newsockfd, buffer, sizeof(buffer));
                bzero(buffer, 256);
                // continue;
            }
            // handleAverage() to calculate average of assignment
            double avg = handleAverage(atoi(token));
            // flushing the buffer
            bzero(buffer, 256);
            // Storing output in buffer
            sprintf(buffer, "%f", avg);
            if (avg < 0.0)
            {
                bzero(buffer, 256);
                // Storing output in buffer
                sprintf(buffer, "%s", "Invalid assignment index!\n");
            }
            // Sending response
            n = write(newsockfd, buffer, sizeof(buffer));
        }
        else if (strcmp(token, "GRADEX") == 0)
        {
            token = strtok(NULL, "\n");
            int rollnum;
            // check whether message is there or not
            if (token == NULL)
            {
                rollnum = -1;
            }
            else
            {
                rollnum = atoi(token);
            }
            // handleGradeX() to calculate grade of the roll number
            char grades[256];
            bzero(grades, 256);
            handleGradeX(grades, rollnum);
            // Sending response
            n = write(newsockfd, grades, sizeof(grades));
        }
        else if (strcmp(buffer, "GRADEX\n") == 0)
        {
            // return grade of all students
            handleGradeXAll(newsockfd);
        }
        else if (strcmp(token, "SORTX") == 0)
        {
            handleSortX(newsockfd, query);
        }
        else if (strncmp(buffer, "RANKX", 5) == 0)
        {
            token = strtok(NULL, "\n");
            int rollnum;
            // check whether message is there or not
            if (token == NULL)
            {
                rollnum = -1;
            }
            else
            {
                rollnum = atoi(token);
                if (rollnum < 0)
                {
                    bzero(buffer, 256);
                    sprintf(buffer, "%s", "Provide valid roll number!\n");
                    n = write(newsockfd, buffer, sizeof(buffer));
                    continue;
                }
            }
            handleRankX(rollnum, newsockfd);
        }
        else if (strcmp(token, "SIMILARX") == 0)
        {
            token = strtok(NULL, "\n");
            int anum;
            // check whether message is there or not
            if (token == NULL)
            {
                bzero(buffer, 256);
                sprintf(buffer, "%s", "Please provide assignment number!");
                int n = write(newsockfd, buffer, sizeof(buffer));
                continue;
            }
            else
            {
                anum = atoi(token);
            }
            // handleGradeX() to calculate grade of the roll number
            handleSimilarX(newsockfd, anum);
        }
        else if (strncmp(buffer, "EXIT", 4) == 0)
        {
            bzero(buffer, 256);
            sprintf(buffer, "%s", "CONNECTION TERMINATED\n");
            n = write(newsockfd, buffer, sizeof(buffer));
            break;
        }
        else
        {
            // send error response
            sprintf(buffer, "%s", "Command not supported!\n");
            n = write(newsockfd, buffer, sizeof(buffer));
        }
        // flushing out buffer
        bzero(buffer, 256);
        // request completion response
        sprintf(buffer, "%s", "done");
        n = write(newsockfd, buffer, sizeof(buffer));
    }
    close(newsockfd);
    close(sockfd);
    return 0;
}