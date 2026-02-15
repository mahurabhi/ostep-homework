#!/usr/bin/env python3
# Plot "fairness" = completion_time(job0) / completion_time(job1)
# for two jobs (both equal length at each data point) using either
# a lottery scheduler or a stride scheduler.

import argparse
import random
import statistics
import matplotlib.pyplot as plt

def parse_args():
    p = argparse.ArgumentParser(description='Compare lottery vs stride fairness')
    p.add_argument('-m', '--mode', choices=('lottery','stride'), default='lottery',
                   help='scheduler to simulate')
    p.add_argument('-t0', '--tickets0', type=int, default=1, help='tickets for job0')
    p.add_argument('-t1', '--tickets1', type=int, default=100, help='tickets for job1')
    p.add_argument('-L', '--maxlen', type=int, default=500, help='max job length to sweep')
    p.add_argument('-s', '--seed', type=int, default=42, help='random seed')
    p.add_argument('-r', '--trials', type=int, default=200, help='trials per length (lottery)')
    return p.parse_args()

args = parse_args()
random.seed(args.seed)

T0 = args.tickets0
T1 = args.tickets1
lengths = list(range(1, args.maxlen + 1))
trials_per_length = args.trials if args.mode == 'lottery' else 1

STRIDE_CONST = 1_000_000.0

def stride_once(len0, len1, t0=T0, t1=T1):
    rem0, rem1 = int(len0), int(len1)
    comp0 = comp1 = None
    time = 0
    stride0 = STRIDE_CONST / float(t0) if t0 > 0 else float('inf')
    stride1 = STRIDE_CONST / float(t1) if t1 > 0 else float('inf')
    pass0 = pass1 = 0.0

    while rem0 > 0 or rem1 > 0:
        if rem0 == 0:
            time += rem1
            comp1 = time
            rem1 = 0
            break
        if rem1 == 0:
            time += rem0
            comp0 = time
            rem0 = 0
            break

        if pass0 <= pass1:
            rem0 -= 1
            time += 1
            pass0 += stride0
            if rem0 == 0 and comp0 is None:
                comp0 = time
        else:
            rem1 -= 1
            time += 1
            pass1 += stride1
            if rem1 == 0 and comp1 is None:
                comp1 = time

    if comp0 is None: comp0 = time
    if comp1 is None: comp1 = time
    return comp0 / comp1

def lottery_once(len0, len1, t0=T0, t1=T1):
    rem0, rem1 = int(len0), int(len1)
    comp0 = comp1 = None
    time = 0
    while rem0 > 0 or rem1 > 0:
        if rem0 == 0:
            time += rem1
            comp1 = time
            rem1 = 0
            break
        if rem1 == 0:
            time += rem0
            comp0 = time
            rem0 = 0
            break

        tickets = (t0 if rem0 > 0 else 0) + (t1 if rem1 > 0 else 0)
        pick = random.randrange(tickets)
        if pick < t0:
            rem0 -= 1
            time += 1
            if rem0 == 0 and comp0 is None:
                comp0 = time
        else:
            rem1 -= 1
            time += 1
            if rem1 == 0 and comp1 is None:
                comp1 = time

    if comp0 is None: comp0 = time
    if comp1 is None: comp1 = time
    return comp0 / comp1

means = []
stdevs = []
for L in lengths:
    vals = []
    for _ in range(trials_per_length):
        if args.mode == 'stride':
            vals.append(stride_once(L, L))
        else:
            vals.append(lottery_once(L, L))
    means.append(statistics.mean(vals))
    stdevs.append(statistics.pstdev(vals) if len(vals) > 1 else 0.0)

plt.figure(figsize=(8,5))
plt.errorbar(lengths, means, yerr=stdevs, fmt='.-', alpha=0.8,
             label=f'{args.mode.capitalize()} fairness (comp0/comp1)')
plt.plot(lengths, [1.0]*len(lengths), 'k--', alpha=0.6, label='Baseline fairness = 1 (equal lengths)')
plt.xlabel('Job0 & Job1 length (time units)')
plt.ylabel('Fairness = completion_time(job0) / completion_time(job1)')
plt.title(f'{args.mode.capitalize()} scheduler fairness vs job length (tickets {T0}:{T1})')
plt.legend()
plt.grid(True)
plt.tight_layout()
out = f'{args.mode}_fairness_vs_length.png'
plt.savefig(out)
print(f'Wrote {out}')
plt.show()