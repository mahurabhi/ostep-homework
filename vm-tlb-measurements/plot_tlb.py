#!/usr/bin/env python3
"""
Plot TLB access times vs number of pages.
Runs tlb_measure with varying page counts and plots the results.
"""

import subprocess
import sys
import matplotlib.pyplot as plt

def run_tlb_measure(num_pages, num_trials):
    """Run tlb_measure and return time per access in nanoseconds."""
    try:
        result = subprocess.run(
            ['./tlb_measure', str(num_pages), str(num_trials)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"Error running tlb_measure: {result.stderr}")
            return None
        
        # Parse output to extract "Time per access (ns): X.XX"
        for line in result.stdout.split('\n'):
            if 'Time per access (ns):' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    return float(parts[1].strip())
        
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    """Main: sweep page counts and measure access times."""
    
    # Parameters
    num_trials = 10000  # trials per measurement
    
    # Page counts to test: powers of 2 and intermediate values
    page_counts = [
        1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536
    ]
    
    print("Measuring TLB access times...")
    print(f"{'Pages':<10} {'Time (ns)':<15} {'Status'}")
    print("-" * 40)
    
    times_ns = []
    pages_tested = []
    
    for num_pages in page_counts:
        time_ns = run_tlb_measure(num_pages, num_trials)
        
        if time_ns is not None:
            times_ns.append(time_ns)
            pages_tested.append(num_pages)
            print(f"{num_pages:<10} {time_ns:<15.2f} ✓")
        else:
            print(f"{num_pages:<10} {'N/A':<15} ✗")
    
    if not times_ns:
        print("Error: No measurements collected.")
        return 1
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(pages_tested, times_ns, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Number of Pages', fontsize=12)
    plt.ylabel('Time per Access (ns)', fontsize=12)
    plt.title('TLB Access Time vs Working Set Size', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    # Annotations for TLB transition
    if len(times_ns) > 1:
        min_time = min(times_ns)
        max_time = max(times_ns)
        tlb_knee = None
        
        # Find the "knee" — where access time increases significantly
        for i in range(1, len(times_ns)):
            if times_ns[i] > times_ns[i-1] * 1.5:  # 50% increase
                tlb_knee = pages_tested[i-1]
                break
        
        if tlb_knee:
            plt.axvline(x=tlb_knee, color='r', linestyle='--', alpha=0.5, label=f'TLB knee ~{tlb_knee} pages')
            plt.legend()
    
    plt.tight_layout()
    plt.savefig('tlb_access_times.png', dpi=150)
    print(f"\nPlot saved to tlb_access_times.png")
    plt.show()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())