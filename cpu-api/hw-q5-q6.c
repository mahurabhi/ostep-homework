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
        printf("The rc of wait in the child is %d\n",wait(NULL));
    }
    else
    {
        printf("The pid of the child is %u\n", process_id);
        // printf("The rc of wait is %d\n",wait(NULL));
        printf("The rc of waitpid is %d\n",waitpid(process_id, NULL, 0));
        printf("Goodbye\n");
    }
}