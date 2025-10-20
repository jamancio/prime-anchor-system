# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 6: The Primorial Filter Showdown
#
# This is the final test of efficiency.
#
# Test 5 proved S_n (r_max=16) is more efficient than a
# Random Mod 6 search (c_max=20).
#
# This test answers the final question:
# Is the S_n sequence's efficiency (r_max=16) special, or can
# it be beaten by a more advanced filter?
#
# We will race System A (S_n) vs. System B (Random Mod 30).
# Mod 30 = 2 * 3 * 5
# ==============================================================================

import math
import time
import random

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
MAX_PRIME_PAIRS_TO_TEST = 50000000      

# Search limits for our two systems
MAX_RADIUS_LIMIT = 30           # System A
RANDOM_SEARCH_LIMIT = 100         # System B

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
def run_primorial_filter_test():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting \"Primorial Filter Showdown\" for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - Testing System A (True S_n) vs. System B (Random Mod 30)")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 6 ---
    total_law_I_failures = 0
    
    # System A (True System)
    true_system_failures = [] 
    max_r_observed = 0
    
    # System B (Mod 30 Random)
    mod30_random_failures = [] 
    max_c_mod30_observed = 0
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Max r: {max_r_observed} | Max c_mod30: {max_c_mod30_observed}", end='\r')

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
            
            # --- 2. Test System A (Law III) ---
            is_true_system_corrected = False
            for r in range(1, MAX_RADIUS_LIMIT + 1):
                s_prev = prime_list[i - r] + prime_list[i - r + 1]
                s_next = prime_list[i + r] + prime_list[i + r + 1]

                if is_clean_k(abs(s_prev - q_prime), prime_set) or is_clean_k(abs(s_next - q_prime), prime_set):
                    is_true_system_corrected = True
                    if r > max_r_observed: max_r_observed = r
                    break 
            
            if not is_true_system_corrected:
                true_system_failures.append(failure_details)
                print("\nFATAL: Law III Falsified. Stopping.")
                break 

            # --- Define Neighborhood for Random Test ---
            avg_gap = (prime_list[i+10] - prime_list[i-10]) / 20 
            neighborhood_radius = int(avg_gap * MAX_RADIUS_LIMIT) 
            if neighborhood_radius <= 0: neighborhood_radius = 500 
            
            # --- 3. Test System B (Mod 30 Random) ---
            is_mod30_random_corrected = False
            for c in range(1, RANDOM_SEARCH_LIMIT + 1):
                rand_offset = random.randint(-neighborhood_radius, neighborhood_radius)
                s_control_base = anchor_sum + rand_offset
                s_control_mod30 = s_control_base - (s_control_base % 30) # Force Mod 30

                if is_clean_k(abs(s_control_mod30 - q_prime), prime_set):
                    is_mod30_random_corrected = True
                    if c > max_c_mod30_observed: max_c_mod30_observed = c
                    break 
            
            if not is_mod30_random_corrected:
                failure_details_b = failure_details.copy()
                failure_details_b['attempts_made'] = RANDOM_SEARCH_LIMIT
                mod30_random_failures.append(failure_details_b)


    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Max r: {max_r_observed} | Max c_mod30: {max_c_mod30_observed}")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 6: PRIMORIAL FILTER SHOWDOWN REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    
    # --- System A Report ---
    print("\n" + "-"*20 + " System A: 'Prime Anchor System' ($S_n$) " + "-"*20)
    print(f"  Total Uncorrected Failures: {len(true_system_failures)}")
    print(f"  Max Correction Radius (r_max): {max_r_observed}")

    # --- System B Report ---
    print("\n" + "-"*20 + " System B: 'Mod 30 Random' Control " + "-"*20)
    print(f"  Total Uncorrected Failures: {len(mod30_random_failures)}")
    print(f"  Max Correction Count (c_max): {max_c_mod30_observed}")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if len(true_system_failures) > 0 or len(mod30_random_failures) > 0:
        print("\n  [VERDICT: FAILED TEST]")
        print("  A failure was found in one of the systems. The 100% correction claim is false.")
    else:
        print("\n  [VERDICT: SHOWDOWN COMPLETE]")
        print("  Both systems provided 100% correction. Now compare efficiency:")
        print(f"\n  System (S_n):   r_max = {max_r_observed}")
        print(f"  Random Mod 30:     c_max = {max_c_mod30_observed}")
        
        if max_r_observed < max_c_mod30_observed:
            print("\n  --> CONCLUSION 1: $S_n$ system is still the MOST EFFICIENT.")
            print("      This is a major finding. It implies the $S_n$ sequence")
            print("      has a built-in efficiency that is *even better* than")
            print("      a powerful Mod 30 filter.")
        elif max_c_mod30_observed < max_r_observed:
            print("\n  --> CONCLUSION 2: The 'Primorial Filter' is the key.")
            print("      The Random Mod 30 search is the new champion.")
            print("      This proves efficiency is *not* a magic property of $S_n,")
            print("      but just a function of using a stronger filter (Mod 30 > Mod 6).")
        else:
            print("\n  --> CONCLUSION 3: The systems are equally efficient.")
            print("      This is the most interesting result. It implies that the")
            print("      $S_n$ sequence is 'naturally' optimized to a Mod 30 level.")

    print("=" * (50 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_primorial_filter_test()