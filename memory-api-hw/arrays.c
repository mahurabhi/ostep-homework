#include <stdio.h>
#include <stdlib.h>
int main()
{
    int *data = malloc(sizeof(int) * 100);
    // undefined behavior, usually causes an exc_breakpoint error, 
    // use clang asan to identify such errors. 
    free(data+50);
    data[100] = 0;
}