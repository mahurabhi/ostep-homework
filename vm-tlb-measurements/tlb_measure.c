#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <pthread.h>
#include <mach/thread_policy.h>
#include <mach/mach_init.h>

#define PAGESIZE (16*1024)
#define JUMP (PAGESIZE / sizeof(int))

// Get current time in microseconds
double get_time_us() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1e6 + tv.tv_usec;
}

int main(int argc, char *argv[])
{
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <num_pages> <num_trials>\n", argv[0]);
        return 1;
    }

    int NUMPAGES = strtol(argv[1], NULL, 10);
    int numtrials = strtol(argv[2], NULL, 10);
    
    if (NUMPAGES <= 0 || numtrials <= 0) {
        fprintf(stderr, "Error: num_pages and num_trials must be > 0\n");
        return 1;
    }

    // Pin this process to a single core (macOS)
    // thread_affinity_policy_data_t policy = { 0 };
    // kern_return_t ret = thread_policy_set(
    //     mach_thread_self(),
    //     THREAD_AFFINITY_POLICY,
    //     (thread_policy_t)&policy,
    //     THREAD_AFFINITY_POLICY_COUNT
    // );
    
    // if (ret != KERN_SUCCESS) {
    //     fprintf(stderr, "Warning: Failed to set thread affinity (ret=%d)\n", ret);
    // } else {
    //     printf("Successfully pinned to core 0\n");
    // }

    // Allocate array: NUMPAGES * PAGESIZE bytes
    int *a = malloc(NUMPAGES * PAGESIZE);
    if (!a) {
        perror("malloc");
        return 1;
    }

    // Warm up (optional: touch all pages to fault them in)
    for (int j = 0; j < NUMPAGES * JUMP; j += JUMP) {
        a[j] = 10;
    }

    // Measure time for repeated access pattern
    double time1 = get_time_us();
    
    for (int trial = 0; trial < numtrials; trial++) {
        for (int i = 0; i < NUMPAGES * JUMP; i += JUMP) {
            a[i] += 1;
        }
    }
    
    double time2 = get_time_us();
    
    // Calculate statistics
    double total_time_us = time2 - time1;
    long total_accesses = (long)NUMPAGES * numtrials;
    double time_per_access_us = total_time_us / total_accesses;
    
    printf("Pages: %d | Trials: %d\n", NUMPAGES, numtrials);
    printf("Total time (us): %.2f\n", total_time_us);
    printf("Total accesses: %ld\n", total_accesses);
    printf("Time per access (us): %.4f\n", time_per_access_us);
    printf("Time per access (ns): %.2f\n", time_per_access_us * 1000.0);
    
    free(a);
    return 0;
}