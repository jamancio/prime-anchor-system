# ==============================================================================
# PRIME ANCHOR SYSTEM - Verifying the S_2=8 Anomaly
#
# This script tests the hypothesis that composite k-values divisible by 3
# (e.g., 9, 15, 21, 27) are *only* produced by the anomalous S_2 anchor
# (S_2 = p_2 + p_3 = 3 + 5 = 8).
#
# We predict:
# 1. The set of composites from S_2 will contain k-values divisible by 3.
# 2. The set of composites from ALL OTHER anchors (S_n, n > 2) will
#    contain ZERO k-values divisible by 3.
# ==============================================================================

import math
import time

# --- Configuration ---
# Use the same prime file your other scripts use
PRIME_INPUT_FILE = "primes_100m.txt" 
# 4 million pairs is more than enough to confirm this arithmetic property
MAX_PRIME_PAIRS_TO_TEST = 4000000      

# --- Function to load primes from a file ---
def load_primes_from_file(filename):
    """Loads a list of primes from a text file."""
    print(f"Loading primes from {filename}...")
    start_time = time.time()
    try:
        with open(filename, 'r') as f:
            # We assume the file starts with 2, 3, 5, ...
            # p_list[0]=2, p_list[1]=3, p_list[2]=5, ...
            prime_list = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        print("Please run the 'generate-primes.py' script first.")
        return None
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes in {end_time - start_time:.2f} seconds.")
    return prime_list

# --- Main Testing Logic ---
def run_s2_anomaly_test():
    """Finds all Law I failures and separates them by their source anchor."""
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None:
        return

    # --- Critical Safety Check ---
    # We need n pairs + the next prime, so N+2 primes.
    # e.g., to test 1 pair (S_2), we need p_2, p_3. (i=1 -> p_list[1], p_list[2])
    # So to test N pairs, we need up to p_list[N], p_list[N+1].
    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + 2
    if len(prime_list) < required_primes_count:
        print("\n" + "="*80)
        print("FATAL ERROR: The loaded prime file is too small for this test.")
        print(f"  - Pairs to test: {MAX_PRIME_PAIRS_TO_TEST:,}")
        print(f"  - Primes required: {required_primes_count:,}")
        print(f"  - Primes loaded:   {len(prime_list):,}")
        print("Please generate a larger prime file before running this test.")
        print("="*80)
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting Law I failure analysis for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print("This test will separate failures from S_2=8 from all other anchors.")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 1 ---
    s2_composites = set()
    other_composites = set()
    
    total_s2_failures = 0
    total_other_failures = 0

    # Per your definition S_n (n >= 2), we start with S_2.
    # In our 0-indexed prime_list:
    # i=0: S_1 = p_list[0] + p_list[1] = 2 + 3 = 5 (We skip this)
    # i=1: S_2 = p_list[1] + p_list[2] = 3 + 5 = 8 (This is our target)
    # i=2: S_3 = p_list[2] + p_list[3] = 5 + 7 = 12 (This is the first "other")
    
    start_index = 1 # Start at i=1 to get S_2
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        # --- Find k_min (Same logic as your script) ---
        min_distance_k = 0
        search_dist = 1
        while True:
            # We only need to check k up to a reasonable bound.
            # If the closest prime is > 1000 away, it's not relevant.
            if search_dist > 1000:
                break 
            
            if (anchor_sum - search_dist) in prime_set or (anchor_sum + search_dist) in prime_set:
                min_distance_k = search_dist
                break
            search_dist += 1
        
        if min_distance_k == 0: continue # Skip if no prime found nearby

        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            # This is the core of Test 1:
            # Log the failure to the correct set.
            if i == 1: 
                # This is the S_2 = 3 + 5 = 8 anchor
                s2_composites.add(min_distance_k)
                total_s2_failures += 1
            else:
                # This is any S_n where n > 2
                other_composites.add(min_distance_k)
                total_other_failures += 1

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 1: S_2 ANOMALY REPORT " + "="*20)

    print("\n" + "-"*20 + " Failures from S_2 = 8 " + "-"*20)
    print(f"Total failures (composite k) found for S_2: {total_s2_failures}")
    print("Unique composite k-values found:")
    print(sorted(list(s2_composites)))

    print("\n" + "-"*20 + " Failures from S_n (n > 2) " + "-"*20)
    print(f"Total failures (composite k) found for all other anchors: {total_other_failures:,}")
    print("Unique composite k-values found (sample, first 20):")
    print(sorted(list(other_composites))[:20])

    # --- Hypothesis Verification ---
    print("\n\n" + "="*20 + " HYPOTHESIS VERIFICATION " + "="*20)
    
    # 1. Find k-values divisible by 3 from S_2
    s2_mod3_failures = {k for k in s2_composites if k % 3 == 0}
    print(f"\n[S_2 = 8] Composite k-values divisible by 3:")
    if s2_mod3_failures:
        print(f"  FOUND: {sorted(list(s2_mod3_failures))}")
    else:
        print("  FOUND: None")
        
    # 2. Find k-values divisible by 3 from ALL OTHER anchors
    other_mod3_failures = {k for k in other_composites if k % 3 == 0}
    print(f"\n[S_n, n>2] Composite k-values divisible by 3:")
    if other_mod3_failures:
        print(f"  FOUND: {sorted(list(other_mod3_failures))}")
    else:
        print("  FOUND: None")

    # 3. Final Conclusion
    print("\n" + "-"*20 + " FINAL CONCLUSION " + "-"*20)
    if not other_mod3_failures:
        print("  [SUCCESS] Hypothesis CONFIRMED.")
        print("  As predicted, k-values divisible by 3 (like 9, 15, 21)")
        print("  are *exclusively* generated by the anomalous S_2=8 anchor.")
        print("  This confirms the 'modulo 6' property is the dominant")
        print("  rule for the rest of the Prime Anchor System.")
    else:
        print("  [FAILURE] Hypothesis REJECTED.")
        print("  The system is more complex. We found k-values divisible by 3")
        print("  originating from anchors other than S_2.")

    print("=" * (44 + len(" HYPOTHESIS VERIFICATION ")))


if __name__ == "__main__":
    run_s2_anomaly_test()
