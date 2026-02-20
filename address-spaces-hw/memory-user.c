#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char * argv[])
{
    int dummy = 0;
    int i = 0;
    char * endp = NULL;
    long int size_mb = strtol(argv[1], &endp, 10) * 1024 * 1024;
    printf("The size in mb is: %lu\n", size_mb);
    size_t nelems = size_mb / sizeof(int);
    int *arr = malloc(size_mb);
    volatile int sink;
    while(1)
    {
        while(i < nelems)
        {
            arr[i] = 1;
            i++;
        }
        i = nelems - 1;
        while(i > 0)
        {
            sink = arr[i];
            i--;
        }
        i = 0;
        sink++;
    }
    free(arr);
}