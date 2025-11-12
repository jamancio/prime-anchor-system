# ==============================================================================
# The Prime Anchor System Tester (Version 12.2 - Fast Load & Full Report)
#
# This version loads a pre-computed prime list to test the complete, three-part
# "Prime Anchor System" conjecture. It includes the full, original reporting
# structure for Laws I, II, and III.
# ==============================================================================

import math
import time

# --- Configuration ---
# -- Generate Prime sets first using generate-primes.py --
PRIME_INPUT_FILE = "primes_100m.txt" 
MAX_PRIME_PAIRS_TO_TEST = 50000000      # Set to your desired test limit
MAX_CORRECTION_RADIUS = 20           # A safe radius for the test

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
        print("Please run the 'generate-primes.py' script first.")
        return None
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes in {end_time - start_time:.2f} seconds.")
    return prime_list

# --- Main Testing Logic ---
def test_correction_law():
    """Tests the hierarchical Law of Correction with robust safety checks."""
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None:
        return

    # --- Critical Safety Check ---
    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_CORRECTION_RADIUS + 2
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

    print(f"\nStarting hierarchical test for the first {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"Maximum correction radius set to: {MAX_CORRECTION_RADIUS}")
    print("-" * 80)
    start_time = time.time()
    
    successful_corrections = []
    correction_failures = []
    counterexample_ks = set()
    max_r_observed = 0
    correction_radius_counts = {}

    start_index = MAX_CORRECTION_RADIUS + 1
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Max r: {max_r_observed} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        min_distance_k = 0
        search_dist = 1
        while True:
            if (anchor_sum - search_dist) in prime_set or (anchor_sum + search_dist) in prime_set:
                min_distance_k = search_dist
                break
            search_dist += 1
        
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            counterexample_ks.add(min_distance_k)
            
            q_prime = 0
            if (anchor_sum - min_distance_k) in prime_set:
                q_prime = anchor_sum - min_distance_k
            else:
                q_prime = anchor_sum + min_distance_k
            
            is_corrected = False
            correction_details = {}
            for radius in range(1, MAX_CORRECTION_RADIUS + 1):
                s_prev = prime_list[i - radius] + prime_list[i - radius + 1]
                k_prev = abs(s_prev - q_prime)
                if k_prev == 1 or k_prev in prime_set:
                    is_corrected = True
                    correction_details = {"corrected_by": f"S_n-{radius}", "radius": radius, "new_k": k_prev}
                
                if not is_corrected:
                    s_next = prime_list[i + radius] + prime_list[i + radius + 1]
                    k_next = abs(s_next - q_prime)
                    if k_next == 1 or k_next in prime_set:
                        is_corrected = True
                        correction_details = {"corrected_by": f"S_n+{radius}", "radius": radius, "new_k": k_next}

                if is_corrected:
                    base_info = {"original_anchor": anchor_sum, "prime_q": q_prime, "composite_k": min_distance_k}
                    successful_corrections.append({**base_info, **correction_details})
                    
                    # Update stats for final report
                    correction_radius_counts[radius] = correction_radius_counts.get(radius, 0) + 1
                    if radius > max_r_observed:
                        max_r_observed = radius
                    break
            
            if not is_corrected:
                correction_failures.append({"original_anchor": anchor_sum, "failed_prime_q": q_prime, "composite_k": min_distance_k})
                break

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Max r: {max_r_observed} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " FINAL ANALYSIS REPORT " + "="*20)
    if not correction_failures:
        print(f"\n[ STATUS: LAW III VERIFIED UP TO {MAX_PRIME_PAIRS_TO_TEST:,} PAIRS ]")
        print(f"The system holds true. All {len(successful_corrections):,} exceptions were successfully corrected.")
        print(f"The maximum correction radius observed was: r_max = {max_r_observed}")
    else:
        print("\n[ STATUS: ANOMALY DETECTED - LAW III FALSIFIED ]")
        # ... (Failure reporting)

    print("\n" + "-"*20 + " Law II Report: Composite k-Values Found " + "-"*20)
    print("The unique composite k-values found in the exceptions were:")
    print(sorted(list(counterexample_ks)))

    print("\n" + "-"*20 + " Law III Report: Correction Radius Distribution " + "-"*20)
    total_exceptions = sum(correction_radius_counts.values())
    print(f"{'Radius (r)':<12} | {'Corrections':<15} | {'Percentage'}")
    print("-" * 50)
    for r in sorted(correction_radius_counts.keys()):
        count = correction_radius_counts[r]
        percentage = (count / total_exceptions) * 100 if total_exceptions > 0 else 0
        print(f"{r:<12} | {count:<15,} | {percentage:.2f}%")
    print("-" * 50)
    print(f"Total Law I Exceptions Found: {total_exceptions:,}")

if __name__ == "__main__":
    test_correction_law()
