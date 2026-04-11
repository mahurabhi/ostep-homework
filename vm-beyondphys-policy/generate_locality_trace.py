#!/usr/bin/env python3
import random
import sys

def main():
    # Usage: ./generate_locality_trace.py [length] [max_page]
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    max_page = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    # 80-20 rule: 80% of references to 20% of pages
    num_hot = max(1, int(max_page * 0.2))
    # Pick random unique hot pages
    hot_pages = random.sample(range(max_page), num_hot)
    
    trace = []
    for _ in range(length):
        if random.random() < 0.8:
            trace.append(str(random.choice(hot_pages)))
        else:
            trace.append(str(random.randint(0, max_page - 1)))
            
    print(",".join(trace))

if __name__ == "__main__":
    main()