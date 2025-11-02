#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>

int main()
{
    int rc = 0;
    int fd;
    pid_t process_id;
    fd = open("hello.txt", O_RDWR | O_CREAT | O_APPEND);
    process_id = fork();
    if(process_id == 0)
    {
        printf("This is from the child\n");
        write(fd, "This is the child\n", 19);
    }
    else
    {
        printf("The pid of the child process is: %u\n", process_id);
        write(fd, "This is the parent\n", 19);
    }
    return 0;
}
