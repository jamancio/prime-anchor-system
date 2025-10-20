# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 10: The "Deterministic Decay" Showdown
# 
# This is the final, most detailed analysis of efficiency.
#
# Test 8 proved the "Perfected Mod 210" system has a vastly
# superior *instant* (r=1) fix rate (94.32% vs 75.85%).
#
# This script will compare the *entire decay curve* for both
# deterministic systems. It will count the number of fixes at
# r=1, r=2, r=3, etc., for both systems, allowing a full
# comparison of their "deterministic decay".
# ==============================================================================

import math
import time
from collections import defaultdict

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
def run_decay_showdown():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting \"Deterministic Decay Showdown\" for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - Comparing the full r=1...r_max decay of S_n vs. Perfected Mod 210")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 10 ---
    total_law_I_failures = 0
    
    # System A (S_n) decay tracking
    s_n_radius_counts = defaultdict(int)
    s_n_failures = []
    max_r_s_n = 0
    
    # System B (Mod 210) decay tracking
    mod210_radius_counts = defaultdict(int)
    mod210_failures = []
    max_r_mod210 = 0
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | S_n r_max: {max_r_s_n} | Mod210 r_max: {max_r_mod210}", end='\r')

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
            
            # --- 2. Run Full Search for System A (S_n) ---
            is_s_n_corrected = False
            for r in range(1, MAX_RADIUS_LIMIT + 1):
                s_prev = prime_list[i - r] + prime_list[i - r + 1]
                s_next = prime_list[i + r] + prime_list[i + r + 1]

                if is_clean_k(abs(s_prev - q_prime), prime_set) or is_clean_k(abs(s_next - q_prime), prime_set):
                    s_n_radius_counts[r] += 1
                    is_s_n_corrected = True
                    if r > max_r_s_n:
                        max_r_s_n = r
                    break 
            
            if not is_s_n_corrected:
                s_n_failures.append(i) # Log the index
                
            # --- 3. Run Full Search for System B (Perfected Mod 210) ---
            is_mod210_corrected = False
            for r in range(1, MAX_RADIUS_LIMIT + 1):
                s_prev_base = prime_list[i - r] + prime_list[i - r + 1]
                s_next_base = prime_list[i + r] + prime_list[i + r + 1]
                
                s_prev_210 = s_prev_base - (s_prev_base % 210)
                s_next_210 = s_next_base - (s_next_base % 210)
            
                if is_clean_k(abs(s_prev_210 - q_prime), prime_set) or is_clean_k(abs(s_next_210 - q_prime), prime_set):
                    mod210_radius_counts[r] += 1
                    is_mod210_corrected = True
                    if r > max_r_mod210:
                        max_r_mod210 = r
                    break 
            
            if not is_mod210_corrected:
                mod210_failures.append(i) # Log the index
            
            # If either system failed, stop
            if s_n_failures or mod210_failures:
                print(f"\nFATAL: A system failed to find a fix. Stopping.")
                break


    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | S_n r_max: {max_r_s_n} | Mod210 r_max: {max_r_mod210}   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 10: \"Deterministic Decay\" REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    
    if s_n_failures or mod210_failures:
        print(f"FATAL: S_n system failed {len(s_n_failures)} times.")
        print(f"FATAL: Mod 210 system failed {len(mod210_failures)} times.")
        return

    print("\n" + "-"*30 + " Correction Radius Distribution " + "-"*30)
    print(f"{'Radius (r)':<12} | {'S_n Fixes':<15} | {'Mod 210 Fixes':<18} | {'S_n Cum. %':<15} | {'Mod 210 Cum. %':<15}")
    print("-" * 80)

    max_r = max(max_r_s_n, max_r_mod210)
    s_n_cumulative_count = 0
    mod210_cumulative_count = 0

    for r in range(1, max_r + 1):
        s_n_count = s_n_radius_counts.get(r, 0)
        mod210_count = mod210_radius_counts.get(r, 0)
        
        s_n_cumulative_count += s_n_count
        mod210_cumulative_count += mod210_count
        
        s_n_cum_percent = (s_n_cumulative_count / total_law_I_failures) * 100
        mod210_cum_percent = (mod210_cumulative_count / total_law_I_failures) * 100
        
        print(f"{r:<12} | {s_n_count:<15,} | {mod210_count:<18,} | {s_n_cum_percent:<15.2f}% | {mod210_cum_percent:<15.2f}%")

    print("-" * 80)
    print(f"{'TOTALS':<12} | {s_n_cumulative_count:<15,} | {mod210_cumulative_count:<18,} | {s_n_cum_percent:<15.2f}% | {mod210_cum_percent:<15.2f}%")
    print("\n" + "-"*30 + " Final r_max Comparison " + "-"*30)
    print(f"  System A (S_n System r_max):     {max_r_s_n}")
    print(f"  System B (Perfected Mod 210):  r_max = {max_r_mod210}")

    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    if max_r_mod210 < max_r_s_n:
        print("\n  [VERDICT: The 'Perfected Mod 210' system is definitively superior.]")
        print("  It is superior in two ways:")
        print(f"  1. It has a *dramatically* faster decay (higher r=1 rate).")
        print(f"  2. It has a *smaller* overall r_max.")
    else:
        print("\n  [VERDICT: The S_n sequence's 'natural' spacing is superior.]")
        print(f"  The S_n system (r_max={max_r_s_n}) is *still* more efficient than, or equal to,")
        print(f"  the 'Perfected Mod 210' system (r_max={max_r_mod210}).")


    print("=" * (50 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_decay_showdown()