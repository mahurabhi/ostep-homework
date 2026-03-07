# Homework Answers — Free‑space Allocation Experiments

## 1. Best‑fit (-p BEST)
**Command**
```
./malloc.py -n 10 -H 0 -p BEST -s 0 -c
```

**Observed free-list (final snapshot)**
```
ptr[0] = Alloc(3) returned 1000 (searched 1 elements)
Free List [ Size 1 ]: [ addr:1003 sz:97 ]

Free(ptr[0]) -> 0
Free List [ Size 2 ]: [ addr:1000 sz:3 ][ addr:1003 sz:97 ]

ptr[1] = Alloc(5) returned 1003 (searched 2 elements)
Free List [ Size 2 ]: [ addr:1000 sz:3 ][ addr:1008 sz:92 ]

Free(ptr[1]) -> 0
Free List [ Size 3 ]: [ addr:1000 sz:3 ][ addr:1003 sz:5 ][ addr:1008 sz:92 ]

ptr[2] = Alloc(8) returned 1008 (searched 3 elements)
Free List [ Size 3 ]: [ addr:1000 sz:3 ][ addr:1003 sz:5 ][ addr:1016 sz:84 ]

Free(ptr[2]) -> 0
Free List [ Size 4 ]: [ addr:1000 sz:3 ][ addr:1003 sz:5 ][ addr:1008 sz:8 ][ addr:1016 sz:84 ]

ptr[3] = Alloc(8) returned 1008 (searched 4 elements)
Free List [ Size 3 ]: [ addr:1000 sz:3 ][ addr:1003 sz:5 ][ addr:1016 sz:84 ]

Free(ptr[3]) -> 0
Free List [ Size 4 ]: [ addr:1000 sz:3 ][ addr:1003 sz:5 ][ addr:1008 sz:8 ][ addr:1016 sz:84 ]

ptr[4] = Alloc(2) returned 1000 (searched 4 elements)
Free List [ Size 4 ]: [ addr:1002 sz:1 ][ addr:1003 sz:5 ][ addr:1008 sz:8 ][ addr:1016 sz:84 ]

ptr[5] = Alloc(7) returned 1008 (searched 4 elements)
Free List [ Size 4 ]: [ addr:1002 sz:1 ][ addr:1003 sz:5 ][ addr:1015 sz:1 ][ addr:1016 sz:84 ]
```

**Analysis (condensed)**
- BEST‑FIT chooses the smallest free block that fits, so it tends to split small holes first and leave large blocks intact.
- Over time this creates many tiny fragments (1‑byte holes in this run).
- Without coalescing these tiny fragments accumulate and increase external fragmentation.

**Takeaway**
- BEST‑FIT can increase the count of tiny free blocks; report metrics (free block count, largest free block, average size) for a quantitative comparison.

---

## 2. Worst‑fit (-p WORST)
**Command**
```
./malloc.py -n 10 -H 0 -p WORST -s 0 -c
```

**Observed free-list (example final snapshot)**
```
Free List [ Size 5 ]: [ addr:1000 sz:3 ] [ addr:1003 sz:5 ] [ addr:1008 sz:8 ] [ addr:1016 sz:8 ] [ addr:1033 sz:67 ]
```

**Analysis (condensed)**
- WORST‑FIT selects the largest free block and splits it, leaving fewer tiny holes initially.
- It consumes the large reservoir faster, producing more medium‑sized fragments and shrinking the largest block.

**Takeaway**
- WORST reduces tiny-fragment count but fragments the large pool; measure the same metrics as above to compare.

---

## 3. First‑fit (-p FIRST)
**Command**
```
./malloc.py -n 10 -H 0 -p FIRST -s 0 -c
```

**Observed behavior (excerpt)**
```
ptr[0] = Alloc(3) returned 1000 (searched 1 elements)
...
ptr[4] = Alloc(2) returned 1000 (searched 1 elements)
ptr[5] = Alloc(7) returned 1008 (searched 3 elements)
```

**Comparison**
- For the 2‑byte and 7‑byte requests in this workload:
  - BEST‑FIT searched 4 elements.
  - FIRST‑FIT searched 1 and 3 elements respectively.
- BEST‑FIT performs more traversal here because it scans for the smallest fitting hole; FIRST‑FIT stops at the first adequate block, often reducing list traversal.

---

## 5. Effect of Coalescing (`-C`)
**Experiment**
- Increase random allocations: `-n 1000`. Run with and without `-C` and collect:
  - number of free blocks
  - largest free block (bytes)
  - average free‑block size
  - count of failed large allocations

**Observations**
- **Without coalescing**
  - Free list grows large and highly fragmented (many 1–2 byte holes).
  - Large allocations begin to fail despite ample total free memory.
  - Search costs increase due to many small blocks.
  - Effect is worse for BEST and WORST policies.
- **With coalescing**
  - Adjacent free blocks are merged, greatly reducing the number of free blocks.
  - Large contiguous regions persist and large allocation requests succeed more often.
  - Search costs are lower.

**Ordering**
- When fragmentation is extreme (many similarly tiny chunks), global ordering of the list has little benefit.
- With coalescing or diverse block sizes, ordering matters:
  - BEST tends to generate many small fragments.
  - WORST tends to preserve larger holes early.
  - FIRST is a reasonable compromise for locality and coalescing.

---

## Is ordering by size bad for FIRST‑FIT?
**Short answer:** Yes — generally.

**Why**
- FIRST‑FIT assumes an address‑ordered list: scanning in address order preserves spatial locality and simplifies coalescing of adjacent blocks.
- Sorting the list by size breaks address order:
  - Adjacent free blocks are not near each other in the list → coalescing becomes harder/expensive.
  - Small‑first ordering causes behavior similar to BEST‑FIT (many small splits).
  - Large‑first ordering makes it behave like WORST‑FIT (consumes big blocks, leaves medium fragments).
- Cache/locality suffers: address order gives better scan locality.

**When size ordering helps**
- If you use BEST/WORST policies, size ordering can speed the search.
- Better option: use segregated free lists (bins) by size class. That keeps address locality within bins (or use per‑bin address ordering) and gives fast searches without global size sorting.

6. What happens when you change the percent allocated fraction -P
to higher than 50? What happens to allocations as it nears 100?
What about as the percent nears 0?

P > 50%:

Most of the heap is already in use, so free regions are smaller and fewer.
Allocators must scan more (more probes) to find fitting holes → higher search cost.
Splitting existing free blocks becomes common, increasing fragmentation unless coalescing mitigates it.
Large allocation requests are more likely to fail or force expensive compaction/merging.
P ≈ 100%:

Virtually no free space left. New allocations will mostly fail immediately.
If any succeed it will be because earlier allocations were freed; success becomes dependent on frees/coalescing.
The simulator will show many allocation failures and little variation across policies (there simply isn’t space).
P ≈ 0%:

Almost all memory is free (one or a few large free regions). Allocations succeed easily and quickly.
Low fragmentation, low search cost (especially for FIRST‑FIT: first large block satisfies requests).
The worst effect is that you don’t exercise fragmentation behavior — results may look uniformly good.

7. What kind of specific requests can you make to generate a highly-
fragmented free space? Use the -A flag to create fragmented free
lists, and see how different policies and options change the organi-
zation of the free list.

Repeatedly allocate and free alternating sizes (e.g., allocate small blocks interleaved with larger blocks, then free every other allocation) produces many small interleaved holes — a highly fragmented free list for FIRST‑FIT.

Concrete -A patterns to generate fragmentation
Checkerboard (many 1‑byte holes):
Trace concept: allocate 16 size‑1 blocks, then free every other: A1,A1,... (16 times) then F0,F2,F4,...
Example (adapt to your simulator -A syntax):
-A "A1,A1,A1,A1,A1,A1,A1,A1,A1,A1,A1,A1,A1,A1,A1,A1,F0,F2,F4,F6,F8,F10,F12,F14"
Alternating small/large:
Trace concept: A8,A1,A8,A1,A8,A1,... then free the large ones: F0,F2,F4,...
Example:
-A "A8,A1,A8,A1,A8,A1,A8,A1,F0,F2,F4,F6"
