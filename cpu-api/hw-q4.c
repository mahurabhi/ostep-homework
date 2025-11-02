#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    pid_t process_id;
    process_id = fork();
    static char * argv[] = {"/bin/ls","-al", NULL};
    if(process_id == 0)
    {
        printf("Hello\n");
        execve(argv[0], argv, NULL);

    }
    else
    {
        wait(NULL);
        printf("Goodbye\n");
    }
}