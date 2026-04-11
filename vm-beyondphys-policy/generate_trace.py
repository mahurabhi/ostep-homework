#!/usr/bin/env python3
import random
import sys

def main():
    # Usage: ./generate_trace.py [length] [max_page]
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    max_page = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    trace = [str(random.randint(0, max_page - 1)) for _ in range(length)]
    print(",".join(trace))

if __name__ == "__main__":
    main()