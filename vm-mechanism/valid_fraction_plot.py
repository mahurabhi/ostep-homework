#!/usr/bin/env python3
# Plot fraction of valid virtual addresses vs. bounds register value.
# Runs the same random VA generator as relocation.py for multiple seeds.

import argparse
import random
import math
import matplotlib.pyplot as plt
import statistics

def convert(size):
    s = str(size)
    if s[-1] in ('k','K'):
        return int(s[:-1]) * 1024
    if s[-1] in ('m','M'):
        return int(s[:-1]) * 1024*1024
    if s[-1] in ('g','G'):
        return int(s[:-1]) * 1024*1024*1024
    return int(s)

def fraction_for_seed(asize, limit_vals, seed, n_addresses):
    random.seed(seed)
    fracs = []
    for limit in limit_vals:
        valid = 0
        for _ in range(n_addresses):
            vaddr = int(asize * random.random())
            if vaddr < limit:
                valid += 1
        fracs.append(valid / n_addresses)
    return fracs

def main():
    p = argparse.ArgumentParser(description='Plot fraction of valid VAs vs bounds register')
    p.add_argument('-a','--asize', default='16k', help='address space size (e.g., 16k)')
    p.add_argument('-n','--num', type=int, default=5000, help='addresses per trial')
    p.add_argument('-S','--seeds', default='0,1,2,3,4', help='comma-separated seeds to run')
    p.add_argument('-p','--points', type=int, default=101, help='number of limit points from 0..ASIZE')
    p.add_argument('-o','--out', default='valid_fraction_vs_limit.png', help='output PNG')
    args = p.parse_args()

    asize = convert(args.asize)
    seeds = [int(x) for x in args.seeds.split(',') if x.strip()!='']
    n = args.num
    points = args.points

    # limit values from 0 .. asize inclusive
    limit_vals = [int(round(i * (asize) / (points-1))) for i in range(points)]

    # run per-seed experiments
    all_fracs = []
    for s in seeds:
        fr = fraction_for_seed(asize, limit_vals, s, n)
        all_fracs.append(fr)

    # compute mean and stdev across seeds
    means = [statistics.mean(col) for col in zip(*all_fracs)]
    stdevs = [statistics.pstdev(col) for col in zip(*all_fracs)]

    # theoretical expectation: limit / asize (use float)
    theory = [lv / asize for lv in limit_vals]

    # plot
    plt.figure(figsize=(8,5))
    for i, s in enumerate(seeds):
        plt.plot(limit_vals, all_fracs[i], alpha=0.5, label=f'seed {s}')
    plt.plot(limit_vals, means, 'k-', lw=2, label='mean (seeds)')
    plt.fill_between(limit_vals,
                     [m - sd for m,sd in zip(means,stdevs)],
                     [m + sd for m,sd in zip(means,stdevs)],
                     color='gray', alpha=0.2, label='±1 stdev')
    plt.plot(limit_vals, theory, 'r--', lw=1.5, label='theoretical = limit / asize')
    plt.xlabel('Bounds register (limit)')
    plt.ylabel('Fraction of valid virtual addresses')
    plt.title(f'Fraction valid VAs vs limit (ASIZE={asize}, {n} addrs/trial)')
    plt.legend(loc='best', fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(args.out)
    print(f'Wrote {args.out}')

if __name__ == '__main__':
    main()