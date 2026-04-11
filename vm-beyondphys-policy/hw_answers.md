1. For a cache of size 5, generate worst-case address reference streams
for each of the following policies: FIFO, LRU, and MRU (worst-case
reference streams cause the most misses possible. For the worst case
reference streams, how much bigger of a cache is needed to improve
performance dramatically and approach OPT?

**FIFO and LRU:**
For a cache size of 5, a worst-case address stream is a looping sequential access over N+1 pages.
Example: `0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, ...`

Both policies yield a **0% hit rate** (after the cache fills) on this stream. Every access evicts the page that will be needed T accesses later, where T is the cache size.

**MRU:**
MRU performs well on looping sequences (where FIFO/LRU fail) but performs poorly on repeated alternating access to the most recently used slot.
Example: `0, 1, 2, 3, 4, 5, 4, 5, 4, 5, ...`

After filling the cache (0-4), accessing 5 evicts 4 (MRU). Accessing 4 evicts 5. This results in a near 0% hit rate for the alternating portion.

**OPT:**
The worst-case trace for the Optimal policy is a sequence with **no temporal locality**, such as a purely sequential scan of unique pages (e.g., `0, 1, 2, 3, ...`). This results in a 0% hit rate because no page is ever revisited.

Unlike FIFO and LRU, OPT is robust against looping patterns. On the N+1 loop that causes 0% hits for FIFO/LRU, OPT achieves a high hit rate by evicting the page that will be used furthest in the future.

**Cache Size Improvement:**
For the worst-case N+1 loop (affecting FIFO/LRU), increasing the cache size by **1** (from 5 to 6) allows the entire working set to fit in memory. This eliminates all capacity misses after the initial warm-up, improving the hit rate to 100% and matching OPT.

2. Generate a random trace (use python or perl). How would you
expect the different policies to perform on such a trace?

**Script:**
```python
import random
# Generate a trace of 100 accesses to 10 pages
print(','.join([str(random.randint(0, 9)) for _ in range(100)]))
```

**Performance:**
- **LRU, FIFO, MRU, RAND:** These policies will perform **similarly**. Because the trace is random, there is no temporal or spatial locality to exploit. Past history (used by LRU) or arrival time (FIFO) does not predict future accesses in a random sequence. Thus, their replacement decisions are effectively equivalent to random selection.
- **OPT:** The Optimal policy will still **outperform** the others. Even without locality, OPT looks ahead to see exactly which pages will be needed soonest. This perfect knowledge allows it to avoid evicting pages that are about to be used, providing a mathematical advantage over policies that must guess.

3. Generate a trace with some locality. How would you expect the different policies to perform?

**Script:**
```python
import random
# 80% of accesses to "hot" pages (subset of 2)
hot_pages = [2, 7] 
trace = []
for _ in range(100):
    if random.random() < 0.8:
        trace.append(str(random.choice(hot_pages)))
    else:
        trace.append(str(random.randint(0, 9)))
print(','.join(trace))
```

**Performance:**
- **LRU:** LRU should perform **very well** (approaching OPT) because it keeps the frequently accessed "hot" pages in the cache.
- **FIFO/RAND:** likely perform **worse** than LRU. FIFO might evict a hot page if it arrived a long time ago (even if used recently), and RAND might evict a hot page by chance.
- **MRU:** Likely performs **poorly** if the hot pages are revisited frequently (MRU evicts the most recently used).

4. How does CLOCK do? How about CLOCK with different numbers of clock bits?

**CLOCK Performance:**
The CLOCK algorithm is designed as an efficient approximation of LRU. Its performance depends heavily on the nature of the trace.

- **On a random trace:** CLOCK will perform similarly to **FIFO and RAND**. Without temporal locality, the "use" bit provides little predictive power. The clock hand will sweep through, clearing bits, and the victim chosen is essentially a page that hasn't been referenced since the last sweep, which is not a strong indicator of future use in a random workload.

- **On a trace with locality:** CLOCK performs **much better**, approaching the effectiveness of **LRU**. Frequently accessed "hot" pages will have their use bit constantly set to 1. When the clock hand encounters a hot page, it clears the bit, but the page is likely to be re-referenced (and its bit set back to 1) before the hand completes a full circle. Cold pages are less likely to be re-referenced, so their use bit will remain 0, making them candidates for eviction.

**Effect of Multiple Clock Bits:**
Increasing the number of clock bits improves CLOCK's ability to approximate LRU, making it a more accurate "aging" or "Not Frequently Used" (NFU) algorithm.

- **With 1 bit:** The algorithm only knows if a page was used in the last "sweep" of the clock hand. It cannot distinguish between a page used just now and one used much earlier within that sweep.

- **With multiple bits (e.g., 8 bits):** The bits can be used as a counter. At each timer interrupt, the use bit is shifted into the most significant bit of the counter for each page, and the counter is shifted right. A page that is frequently used will have more `1`s in its counter, resulting in a higher value. The page with the lowest counter value is the best candidate for eviction, as it is the least frequently/recently used.

In summary, **more clock bits allow for a more fine-grained history of page usage**, leading to better replacement decisions on workloads with locality. The performance gain is significant when moving from 1 to a few bits, with diminishing returns as more bits are added. The performance on a purely random trace remains largely unaffected.
