# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 2: The Modulo 6 Classifier
#
# Test 1 proved our "modulo 6" theory was incomplete.
# This test will verify the *complete* theory.
#
# New Hypothesis:
# 1. Failures where k is divisible by 3 (9, 15, 21...) will ONLY come
#    from anchors where S_n % 6 == 2 or S_n % 6 == 4.
# 2. Failures where k is NOT divisible by 3 (25, 35, 49...) will ONLY come
#    from anchors where S_n % 6 == 0.
#
# This test will sort every composite-k failure into one of these bins.
# ==============================================================================

import math
import time
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
MAX_PRIME_PAIRS_TO_TEST = 4000000      

# --- Function to load primes from a file ---
def load_primes_from_file(filename):
    """Loads a list of primes from a text file."""
    print(f"Loading primes from {filename}...")
    start_time = time.time()
    try:
        with open(filename, 'r') as f:
            prime_list = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        return None
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes in {end_time - start_time:.2f} seconds.")
    return prime_list

# --- Main Testing Logic ---
def run_mod6_classifier_test():
    """Finds all Law I failures and classifies them by S_n % 6."""
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting Modulo 6 Classifier test for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 2 ---
    # We will store the *set* of unique k-values found for each bin
    failure_bins = {
        0: defaultdict(int), # S_n % 6 == 0
        2: defaultdict(int), # S_n % 6 == 2
        4: defaultdict(int)  # S_n % 6 == 4
        # S_n % 6 can't be 1, 3, 5 (sum of two odd primes > 3)
    }
    
    total_failures = 0
    
    # Start at i=2 (S_3 = 5+7=12) since we know S_2 (i=1) never fails
    # and S_1 (i=0) is 2+3=5, which is also not part of the n>2 system.
    start_index = 2 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        min_distance_k = 0
        search_dist = 1
        while True:
            if search_dist > 1000: break # Safety break
            
            if (anchor_sum - search_dist) in prime_set or (anchor_sum + search_dist) in prime_set:
                min_distance_k = search_dist
                break
            search_dist += 1
        
        if min_distance_k == 0: continue 

        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            total_failures += 1
            
            # This is the core of Test 2:
            # Classify the failure based on the anchor's mod 6 value
            anchor_mod_6 = anchor_sum % 6
            
            # Log the frequency of this specific k-value in its bin
            failure_bins[anchor_mod_6][min_distance_k] += 1
            

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 2: MODULO 6 CLASSIFIER REPORT " + "="*20)
    print(f"Total Law I Failures (Composite k) Found: {total_failures:,}")

    # --- Report for Bin 0 (S_n % 6 == 0) ---
    print("\n" + "-"*20 + " Failures from S_n % 6 == 0 " + "-"*20)
    bin_0_composites = failure_bins[0].keys()
    print(f"Total failures in this bin: {sum(failure_bins[0].values()):,}")
    print(f"Unique composite k-values (Sample): {sorted(list(bin_0_composites))[:20]}")
    
    mod_3_found_in_bin_0 = {k for k in bin_0_composites if k % 3 == 0}
    if not mod_3_found_in_bin_0:
        print("  [VERIFIED] No k-values divisible by 3 were found.")
    else:
        print(f"  [HYPOTHESIS FAILED] Found k-values divisible by 3: {mod_3_found_in_bin_0}")


    # --- Report for Bin 2 (S_n % 6 == 2) ---
    print("\n" + "-"*20 + " Failures from S_n % 6 == 2 " + "-"*20)
    bin_2_composites = failure_bins[2].keys()
    print(f"Total failures in this bin: {sum(failure_bins[2].values()):,}")
    print(f"Unique composite k-values (Sample): {sorted(list(bin_2_composites))[:20]}")
    
    non_mod_3_found_in_bin_2 = {k for k in bin_2_composites if k % 3 != 0}
    if not non_mod_3_found_in_bin_2:
        print("  [VERIFIED] ALL k-values found were divisible by 3.")
    else:
        print(f"  [HYPOTHESIS FAILED] Found k-values NOT divisible by 3: {non_mod_3_found_in_bin_2}")

    # --- Report for Bin 4 (S_n % 6 == 4) ---
    print("\n" + "-"*20 + " Failures from S_n % 6 == 4 " + "-"*20)
    bin_4_composites = failure_bins[4].keys()
    print(f"Total failures in this bin: {sum(failure_bins[4].values()):,}")
    print(f"Unique composite k-values (Sample): {sorted(list(bin_4_composites))[:20]}")

    non_mod_3_found_in_bin_4 = {k for k in bin_4_composites if k % 3 != 0}
    if not non_mod_3_found_in_bin_4:
        print("  [VERIFIED] ALL k-values found were divisible by 3.")
    else:
        print(f"  [HYPOTHESIS FAILED] Found k-values NOT divisible by 3: {non_mod_3_found_in_bin_4}")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    if not mod_3_found_in_bin_0 and not non_mod_3_found_in_bin_2 and not non_mod_3_found_in_bin_4:
        print("  [SUCCESS] Hypothesis CONFIRMED.")
        print("  The Law I failure mechanism is fully explained by S_n % 6.")
        print("  - S_n % 6 == 0 anchors ONLY produce k % 3 != 0 failures (25, 35...).")
        print("  - S_n % 6 == 2/4 anchors ONLY produce k % 3 == 0 failures (9, 15...).")
        print("\n  This is the complete Law I/II structure.")
    else:
        print("  [FAILURE] Hypothesis REJECTED.")
        print("  The structure is even more complex than predicted.")
        print("  Review the failed bins above to see the anomalies.")

    print("=" * (44 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_mod6_classifier_test()
