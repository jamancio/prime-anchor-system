# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 8: The "Deterministic r=1" Showdown
#
# This is the final test of r=1 efficiency.
#
# It compares two deterministic systems head-to-head:
# 1. System A (S_n): Checks the "natural" anchors S_{n-1} and S_{n+1}.
# 2. System B (Perfected Mod 210): Checks "perfect" anchors by rounding
#    S_{n-1} and S_{n+1} down to the nearest multiple of 210.
#
# It also tracks the *overall* r_max of System A in the background
# to provide progress and confirm previous findings.
# ==============================================================================

import math
import time
import random

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
# 50M pairs is the definitive test
MAX_PRIME_PAIRS_TO_TEST = 50000000      

# We need this to track the *overall* r_max
MAX_RADIUS_LIMIT = 30           

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
def run_deterministic_showdown():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting \"Deterministic r=1 Showdown\" for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - Comparing r=1 success rate of S_n vs. Perfected Mod 210")
    print(f"  - Also tracking overall S_n r_max up to {MAX_RADIUS_LIMIT}...")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 8 ---
    total_law_I_failures = 0
    
    # System A (S_n) r=1 success counter
    system_A_r1_success = 0
    
    # System B (Mod 210) r=1 success counter
    system_B_r1_success = 0
    
    # Background r_max tracking
    max_r_observed = 0
    true_system_failures = [] # Should remain 0
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Current r_max: {max_r_observed}", end='\r')

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
            
            # --- 2. Test System A ($S_n$ at r=1) ---
            s_prev_1 = prime_list[i - 1] + prime_list[i]
            s_next_1 = prime_list[i + 1] + prime_list[i + 2]
            
            if is_clean_k(abs(s_prev_1 - q_prime), prime_set) or is_clean_k(abs(s_next_1 - q_prime), prime_set):
                system_A_r1_success += 1

            # --- 3. Test System B (Deterministic Mod 210 at r=1) ---
            # We use the *same* S_n-1 and S_n+1 anchors as the base
            s_prev_210 = s_prev_1 - (s_prev_1 % 210)
            s_next_210 = s_next_1 - (s_next_1 % 210)
            
            if is_clean_k(abs(s_prev_210 - q_prime), prime_set) or is_clean_k(abs(s_next_210 - q_prime), prime_set):
                system_B_r1_success += 1

            # --- 4. Background Full r_max check for System A (for progress) ---
            # This logic runs in parallel just to confirm our old r_max
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
                true_system_failures.append(i) # Log the index of the failure
                print(f"\nFATAL: Law III Falsified for S_n at index {i}. Stopping.")
                break 

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Final r_max: {max_r_observed}   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 8: \"Deterministic r=1\" REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    print(f"Overall S_n System r_max (Confirmation): {max_r_observed}")
    if true_system_failures:
        print(f"FATAL: S_n system failed {len(true_system_failures)} times.")
    
    # --- Calculate Percentages ---
    rate_A = (system_A_r1_success / total_law_I_failures) * 100
    rate_B = (system_B_r1_success / total_law_I_failures) * 100

    print("\n" + "-"*20 + " Instant Fix Rate (r=1) by System " + "-"*20)
    print(f"  System A ($S_n$):       {rate_A:.2f}%  ({system_A_r1_success:,} fixes)")
    print(f"  System B (Perfected Mod 210): {rate_B:.2f}%  ({system_B_r1_success:,} fixes)")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if rate_B > rate_A:
        print("\n  [VERDICT: The 'Primorial Filter' is the key to efficiency.]")
        print("  The 'Perfected Mod 210' system has a *higher* instant fix rate.")
        print("  This confirms that the $S_n$ system is not the most efficient")
        print("  r=1 path, and that a stronger primorial filter is better.")
    elif rate_A > rate_B:
        print("\n  [VERDICT: The $S_n$ sequence's 'natural' spacing is superior.]")
        print("  The 'S_n' system has a *higher* instant fix rate.")
        print("  This is a major finding: the 'natural' spacing of $S_n$ anchors")
        print("  is *more efficient* than an 'artificial' primorial filter.")
    else:
        print("\n  [VERDICT: The systems are equally efficient.]")
        print("  The fix rates are statistically identical. This implies")
        print("  the $S_n$ sequence is 'naturally' optimized to a Mod 210 level,")
        print("  but is not superior to it.")

    print("=" * (50 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_deterministic_showdown()