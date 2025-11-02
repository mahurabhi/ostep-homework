#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    pid_t process_id0;
    pid_t process_id1;
    int pipefd[2];
    char buffer[13] = "Hello from 0";
    pipe(pipefd);
    process_id0 = fork();
    if(process_id0 == 0)
    {
        // child1
        printf("Hello from child1\n");
        read(pipefd[0], buffer, 13);
        printf("Data read from buffer is : \"%s\"\n", buffer);
    }
    else
    {
        process_id1 = fork();
        if(process_id1 == 0)
        {
            // child2
            printf("Hello from child2\n");
            write(pipefd[1], buffer, 13);
        }
        else
        {
            // parent
            int rc = INT8_MAX;
            while(rc > 0)
            {
                rc = wait(NULL);
                printf("rc of wait is: %d\n", rc);
            }
            printf("All childs have exited \n");
        }
    }
    return 0;
}