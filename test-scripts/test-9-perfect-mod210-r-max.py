# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 9: The "Mod 210 r_max" Test
#
# This is the final, definitive test of efficiency.
#
# Test 8 proved that a "Perfected Mod 210" system has a vastly
# superior *instant* (r=1) fix rate of 94.32%.
#
# This script answers the final question: What is the
# *overall* r_max for this "Perfected Mod 210" system?
#
# We hypothesize its r_max will be significantly smaller than the
# S_n system's r_max of 16.
# ==============================================================================

import math
import time
import random

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
# 50M pairs is the definitive test
MAX_PRIME_PAIRS_TO_TEST = 50000000      

# We'll use the same search limit as before
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
def run_mod210_r_max_test():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting \"Mod 210 r_max Test\" for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - Searching for the max r_max of the Perfected Mod 210 system...")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 9 ---
    total_law_I_failures = 0
    
    # System B (Mod 210) r_max tracking
    max_r_mod210_observed = 0
    mod210_system_failures = [] # Should remain 0
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Current Mod 210 r_max: {max_r_mod210_observed}", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        # --- 1. Find a Law I Failure (using S_n as the "detector") ---
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
            
            # --- 2. Test System B (Perfected Mod 210) for its *full* r_max ---
            is_mod210_corrected = False
            for r in range(1, MAX_RADIUS_LIMIT + 1):
                
                # Get the base S_n anchors at this radius
                s_prev_base = prime_list[i - r] + prime_list[i - r + 1]
                s_next_base = prime_list[i + r] + prime_list[i + r + 1]

                # Convert them to "perfected" Mod 210 anchors
                s_prev_210 = s_prev_base - (s_prev_base % 210)
                s_next_210 = s_next_base - (s_next_base % 210)
            
                if is_clean_k(abs(s_prev_210 - q_prime), prime_set) or is_clean_k(abs(s_next_210 - q_prime), prime_set):
                    is_mod210_corrected = True
                    if r > max_r_mod210_observed:
                        max_r_mod210_observed = r
                    break # Found the fix, stop searching this radius
            
            if not is_mod210_corrected:
                mod210_system_failures.append(i) # Log the index of the failure
                print(f"\nFATAL: Mod 210 system failed at index {i}. Stopping.")
                break 

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Final Mod 210 r_max: {max_r_mod210_observed}   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 9: \"Mod 210 r_max\" REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    if mod210_system_failures:
        print(f"FATAL: Mod 210 system failed {len(mod210_system_failures)} times.")
    
    print("\n" + "-"*20 + " Max Search Depth (r_max) Comparison " + "-"*20)
    print(f"  System A (S_n System r_max):     16 (from Test 8)")
    print(f"  System B (Perfected Mod 210):  r_max = {max_r_mod210_observed}")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if max_r_mod210_observed < 16:
        print("\n  [VERDICT: The 'Primorial Filter' is the key to efficiency.]")
        print("  The 'Perfected Mod 210' system is definitively more efficient,")
        print(f"  with an r_max of {max_r_mod210_observed} (compared to S_n's r_max of 16).")
        print("  This proves the S_n system's efficiency is not unique,")
        print("  and that a stronger filter is superior.")
    else:
        print("\n  [VERDICT: The S_n sequence's 'natural' spacing is superior.]")
        print(f"  The S_n system (r_max=16) is *still* more efficient than, or equal to,")
        print(f"  the 'Perfected Mod 210' system (r_max={max_r_mod210_observed}).")
        print("  This is a major finding, implying the 'natural' spacing of S_n")
        print("  is a uniquely optimized path.")

    print("=" * (50 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_mod210_r_max_test()