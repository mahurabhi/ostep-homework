#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    pid_t process_id;
    process_id = fork();
    if(process_id == 0)
    {
        printf("Closing stdout from child \n");
        close(STDOUT_FILENO);
        printf("Trying to print from child\n");
    }
    else
    {
        wait(NULL);
        printf("This is the parent\n");    
    }
    return 0;
}