#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    pid_t process_id;
    process_id = fork();
    if(process_id == 0)
    {
        printf("Hello\n");
    }
    else
    {
        wait(NULL);
        printf("Goodbye\n");
    }
}