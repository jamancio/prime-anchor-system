# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 4: The FINAL "r_max vs c_max" Showdown
#
# This is the definitive, make-or-break test of the entire Law III conjecture.
#
# This script compares the MAXIMUM SEARCH DEPTH of both systems:
# 1. Your System: What is the maximum RADIUS (r_max) needed to find a fix?
# 2. Random System: What is the maximum COUNT (c_max) of random anchors
#    needed to find a fix?
#
# ==============================================================================

import math
import time
import random

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 

# We must use the 50M test to match your v8.0 data
MAX_PRIME_PAIRS_TO_TEST = 50000000      

# Per v8.0, r_max=16. We set our limit higher to be safe.
MAX_RADIUS_LIMIT = 30           

# We will give the random system a VERY generous search limit
# to prove it has "holes" if it fails.
RANDOM_SEARCH_LIMIT = 100         

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

def is_clean_k(k_val, prime_set):
    """Helper function to check if k is 1 or a prime."""
    if k_val == 1:
        return True
    if k_val in prime_set:
        return True
    return False

# --- Main Testing Logic ---
def run_final_showdown():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting \"Final Showdown\" for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - True System Search Limit: r = {MAX_RADIUS_LIMIT}")
    print(f"  - Random System Search Limit: {RANDOM_SEARCH_LIMIT} attempts")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 4 ---
    total_law_I_failures = 0
    
    # System A (True System)
    true_system_failures = [] # List to store uncorrected failures
    max_r_observed = 0
    
    # System B (Random System)
    random_system_failures = [] # List to store uncorrected failures
    max_c_observed = 0 # << Track max *count* for random
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Failures: {total_law_I_failures:,} | Max r: {max_r_observed} | Max c: {max_c_observed} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        # --- 1. Find a Law I Failure ---
        min_distance_k = 0
        q_prime = 0
        search_dist = 1
        while True:
            if search_dist > 2000: break 
            
            q_lower = anchor_sum - search_dist
            q_upper = anchor_sum + search_dist

            if q_lower in prime_set:
                min_distance_k = search_dist
                q_prime = q_lower
                break
            if q_upper in prime_set:
                min_distance_k = search_dist
                q_prime = q_upper
                break
            search_dist += 1
        
        if min_distance_k == 0: continue 

        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            total_law_I_failures += 1
            failure_details = {
                "n_index": i, 
                "S_n": anchor_sum, 
                "q_prime": q_prime, 
                "k_composite": min_distance_k
            }
            
            # --- 2. Test System A (Your Law III) ---
            is_true_system_corrected = False
            for r in range(1, MAX_RADIUS_LIMIT + 1):
                s_prev = prime_list[i - r] + prime_list[i - r + 1]
                s_next = prime_list[i + r] + prime_list[i + r + 1]

                if is_clean_k(abs(s_prev - q_prime), prime_set) or is_clean_k(abs(s_next - q_prime), prime_set):
                    is_true_system_corrected = True
                    if r > max_r_observed:
                        max_r_observed = r
                    break 
            
            if not is_true_system_corrected:
                true_system_failures.append(failure_details)
                print("\n" + "="*80)
                print(f"FATAL: Law III Falsified at index {i}. See report.")
                print("Stopping test...")
                print("="*88)
                break 

            # --- 3. Test System B (Random Control) ---
            avg_gap = (prime_list[i+10] - prime_list[i-10]) / 20 
            neighborhood_radius = int(avg_gap * MAX_RADIUS_LIMIT) 
            if neighborhood_radius <= 0: neighborhood_radius = 500 
            
            is_random_system_corrected = False
            for c in range(1, RANDOM_SEARCH_LIMIT + 1):
                rand_offset = random.randint(-neighborhood_radius, neighborhood_radius)
                s_control_base = anchor_sum + rand_offset
                s_control_mod6 = s_control_base - (s_control_base % 6)

                if is_clean_k(abs(s_control_mod6 - q_prime), prime_set):
                    is_random_system_corrected = True
                    if c > max_c_observed:
                        max_c_observed = c
                    break 
            
            if not is_random_system_corrected:
                failure_details['attempts_made'] = RANDOM_SEARCH_LIMIT
                random_system_failures.append(failure_details)


    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Failures: {total_law_I_failures:,} | Max r: {max_r_observed} | Max c: {max_c_observed} | Time: {time.time() - start_time:.0f}s")
    
    
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 4: \"Final Showdown\" REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    
    # --- True System Report ---
    print("\n" + "-"*20 + " System A: 'Prime Anchor System' (Your Law III) " + "-"*20)
    print(f"  Total Uncorrected Failures: {len(true_system_failures)}")
    print(f"  Max Correction Radius (r_max): {max_r_observed}")
    if true_system_failures:
        print("\n  FAILURE DETAILS (First Event):")
        print(f"  {true_system_failures[0]}")

    # --- Control System Report ---
    print("\n" + "-"*20 + " System B: 'Random Control' (Null Hypothesis) " + "-"*20)
    print(f"  Total Uncorrected Failures: {len(random_system_failures)}")
    print(f"  Max Correction Count (c_max): {max_c_observed}")
    if random_system_failures:
        print("\n  FAILURE DETAILS (First Event):")
        print(f"  {random_system_failures[0]}")

    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION (THE 'MAKE OR BREAK') " + "="*20)
    
    if len(true_system_failures) > 0:
        print("\n  [VERDICT: BREAK (FALSIFIED)]")
        print("  Law III has been FALSIFIED.")
        print("  The 'Prime Anchor System' is NOT 100% self-correcting.")
        print("  A failure was found that could not be corrected within")
        print(f"  the search limit of r = {MAX_RADIUS_LIMIT}.")

    elif len(true_system_failures) == 0 and len(random_system_failures) > 0:
        print("\n  [VERDICT: MAKE (LAW III is VERIFIED)]")
        print("  This is a SUCCESS. Law III is a real, structural phenomenon.")
        print("  - Your system provided 100% correction.")
        print(f"  - The random system FAILED {len(random_system_failures):,} times, proving it has 'holes'.")
        print("\n  This proves the S_n sequence is a non-random, complete,")
        print("  and structurally constrained corrective system.")

    elif len(true_system_failures) == 0 and len(random_system_failures) == 0:
        print("\n  [VERDICT: BREAK (ARTIFACT)]")
        print("  Law III is an ARTIFACT of a dense neighborhood.")
        print(f"  - Your system provided 100% correction with r_max = {max_r_observed}.")
        print(f"  - The random system ALSO provided 100% correction with c_max = {max_c_observed}.")
        print("\n  This proves the S_n sequence is not special.")
        print("  The 'r_max Mystery' is solved: r_max is small simply")
        print("  because the 'fix' is always nearby for *any* search.")

    print("=" * (50 + len(" FINAL CONCLUSION (THE 'MAKE OR BREAK') ")))


if __name__ == "__main__":
    run_final_showdown()
