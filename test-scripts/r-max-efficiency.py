# ==============================================================================
# ANALYSIS: Comprehensive Efficiency Showdown (v9.1 Data Generator)
#
# This single script gathers all data needed for the final v9.1 paper.
# It runs the relevant comparisons from Tests 6, 7, 8, 9, and 10.
#
# For each Law I failure, it compares:
# 1. System A (S_n): Full deterministic search (r=1 to r_max)
# 2. System B (Random Mod 30): Full random search (c=1 to c_max)
# 3. System C (Perfected Mod 210): Full deterministic search (r=1 to r_max)
# 4. Instant Fix Checks (c=1): For Random Mod 6, Mod 30, Mod 210.
#
# Output matches the tables and conclusions in the v9.1 paper.
# ==============================================================================

import math
import time
from collections import defaultdict
import random

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
# 50M pairs is the definitive test
MAX_PRIME_PAIRS_TO_TEST = 50000000      

# Set a safe search limit for deterministic systems
MAX_RADIUS_LIMIT = 30           
# Set a safe search limit for random systems
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
def run_comprehensive_showdown():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting Comprehensive Showdown for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - Comparing S_n vs. Random Mod 30 vs. Perfected Mod 210")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for the test ---
    total_law_I_failures = 0
    
    # System A (S_n) tracking
    s_n_radius_counts = defaultdict(int)
    s_n_failures = []
    max_r_s_n = 0
    
    # System B (Random Mod 30) tracking
    mod30_random_failures = [] 
    max_c_mod30 = 0
    
    # System C (Perfected Mod 210) tracking
    mod210_radius_counts = defaultdict(int)
    mod210_failures = []
    max_r_mod210 = 0
    
    # Instant Fix (c=1) counters for random systems
    mod6_c1_success = 0
    mod30_c1_success = 0
    mod210_c1_success = 0
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            # Update progress with all max values
            print(f"Progress: {i:,}/{MAX_PRIME_PAIRS_TO_TEST:,} | Fails:{total_law_I_failures:,} | r_Sn:{max_r_s_n} | c_M30:{max_c_mod30} | r_M210:{max_r_mod210}", end='\r')

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
            failure_details = { "n_index": i, "S_n": anchor_sum, "q_prime": q_prime, "k_composite": min_distance_k }
            
            # --- 2. Run Full Search for System A (S_n) ---
            is_s_n_corrected = False
            for r in range(1, MAX_RADIUS_LIMIT + 1):
                s_prev = prime_list[i - r] + prime_list[i - r + 1]
                s_next = prime_list[i + r] + prime_list[i + r + 1]
                if is_clean_k(abs(s_prev - q_prime), prime_set) or is_clean_k(abs(s_next - q_prime), prime_set):
                    s_n_radius_counts[r] += 1
                    is_s_n_corrected = True
                    if r > max_r_s_n: max_r_s_n = r
                    break 
            if not is_s_n_corrected: s_n_failures.append(i)
                
            # --- 3. Run Full Search for System C (Perfected Mod 210) ---
            is_mod210_corrected = False
            for r in range(1, MAX_RADIUS_LIMIT + 1):
                s_prev_base = prime_list[i - r] + prime_list[i - r + 1]
                s_next_base = prime_list[i + r] + prime_list[i + r + 1]
                s_prev_210 = s_prev_base - (s_prev_base % 210)
                s_next_210 = s_next_base - (s_next_base % 210)
                if is_clean_k(abs(s_prev_210 - q_prime), prime_set) or is_clean_k(abs(s_next_210 - q_prime), prime_set):
                    mod210_radius_counts[r] += 1
                    is_mod210_corrected = True
                    if r > max_r_mod210: max_r_mod210 = r
                    break 
            if not is_mod210_corrected: mod210_failures.append(i)
                
            # --- Define Neighborhood for Random Tests ---
            avg_gap = (prime_list[i+10] - prime_list[i-10]) / 20 
            # Use the largest observed r_max to define neighborhood size dynamically
            current_max_r = max(max_r_s_n, max_r_mod210, 1) # Ensure at least 1
            neighborhood_radius = int(avg_gap * current_max_r * 1.5) # Add 50% buffer
            if neighborhood_radius <= 0: neighborhood_radius = 500 

            # --- 4. Run Full Search for System B (Random Mod 30) ---
            is_mod30_random_corrected = False
            for c in range(1, RANDOM_SEARCH_LIMIT + 1):
                rand_offset = random.randint(-neighborhood_radius, neighborhood_radius)
                s_control_base = anchor_sum + rand_offset
                s_control_mod30 = s_control_base - (s_control_base % 30)
                if is_clean_k(abs(s_control_mod30 - q_prime), prime_set):
                    is_mod30_random_corrected = True
                    if c > max_c_mod30: max_c_mod30 = c
                    # Check if this was the *first* attempt (c=1) for instant rate
                    if c == 1: mod30_c1_success += 1
                    break 
            if not is_mod30_random_corrected: mod30_random_failures.append(i)

            # --- 5. Run c=1 Checks for Other Random Systems ---
            # Mod 6
            rand_offset_6 = random.randint(-neighborhood_radius, neighborhood_radius)
            s_control_base_6 = anchor_sum + rand_offset_6
            s_control_mod6 = s_control_base_6 - (s_control_base_6 % 6) 
            if is_clean_k(abs(s_control_mod6 - q_prime), prime_set): mod6_c1_success += 1
                
            # Mod 210
            rand_offset_210 = random.randint(-neighborhood_radius, neighborhood_radius)
            s_control_base_210 = anchor_sum + rand_offset_210
            s_control_mod210 = s_control_base_210 - (s_control_base_210 % 210) 
            if is_clean_k(abs(s_control_mod210 - q_prime), prime_set): mod210_c1_success += 1

            # If any system failed, stop
            if s_n_failures or mod210_failures or mod30_random_failures:
                print(f"\nFATAL: A system failed to find a fix. Stopping.")
                break

    # Final progress print
    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,}/{MAX_PRIME_PAIRS_TO_TEST:,} | Fails:{total_law_I_failures:,} | r_Sn:{max_r_s_n} | c_M30:{max_c_mod30} | r_M210:{max_r_mod210}   ")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " FINAL COMPREHENSIVE ANALYSIS REPORT (v9.1 Data) " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    
    # Check for fatal errors
    if s_n_failures or mod210_failures or mod30_random_failures:
        print(f"FATAL: S_n system failed {len(s_n_failures)} times.")
        print(f"FATAL: Mod 30 Random system failed {len(mod30_random_failures)} times.")
        print(f"FATAL: Mod 210 Perfected system failed {len(mod210_failures)} times.")
        return

    # --- Report 1: Instant Fix Rate Comparison (Data for Table 1 in v9.1) ---
    print("\n" + "-"*30 + " Instant Fix Rate (r=1 / c=1) Comparison " + "-"*30)
    # Calculate percentages
    rate_A_r1 = (s_n_radius_counts.get(1, 0) / total_law_I_failures) * 100
    rate_B_c1 = (mod6_c1_success / total_law_I_failures) * 100 # Random Mod 6
    rate_C_c1 = (mod30_c1_success / total_law_I_failures) * 100 # Random Mod 30
    rate_D_c1 = (mod210_c1_success / total_law_I_failures) * 100 # Random Mod 210
    rate_E_r1 = (mod210_radius_counts.get(1, 0) / total_law_I_failures) * 100 # Perfected Mod 210

    print(f"  System (S_n):                       {rate_A_r1:.2f}% (r=1)")
    print(f"  System (Random Mod 6):              {rate_B_c1:.2f}% (c=1)")
    print(f"  System (Random Mod 30):             {rate_C_c1:.2f}% (c=1)")
    print(f"  System (Random Mod 210):            {rate_D_c1:.2f}% (c=1)")
    print(f"  System (Perfected Mod 210):         {rate_E_r1:.2f}% (r=1)")

    # --- Report 2: Decay Curve Comparison (Data for Table 2 / Text in v9.1) ---
    print("\n" + "-"*30 + " Correction Radius Distribution (S_n vs Perfected Mod 210) " + "-"*30)
    print(f"{'Radius (r)':<12} | {'S_n Fixes':<15} | {'Mod 210 Fixes':<18} | {'S_n Cum. %':<15} | {'Mod 210 Cum. %':<15}")
    print("-" * 80)
    max_r_overall = max(max_r_s_n, max_r_mod210)
    s_n_cumulative_count = 0
    mod210_cumulative_count = 0
    for r in range(1, max_r_overall + 1):
        s_n_count = s_n_radius_counts.get(r, 0)
        mod210_count = mod210_radius_counts.get(r, 0)
        s_n_cumulative_count += s_n_count
        mod210_cumulative_count += mod210_count
        s_n_cum_percent = (s_n_cumulative_count / total_law_I_failures) * 100
        mod210_cum_percent = (mod210_cumulative_count / total_law_I_failures) * 100
        print(f"{r:<12} | {s_n_count:<15,} | {mod210_count:<18,} | {s_n_cum_percent:<15.2f}% | {mod210_cum_percent:<15.2f}%")
    print("-" * 80)
    print(f"{'TOTALS':<12} | {s_n_cumulative_count:<15,} | {mod210_cumulative_count:<18,} | {s_n_cum_percent:<15.2f}% | {mod210_cum_percent:<15.2f}%")

    # --- Report 3: Final Max Search Depth Comparison (Data for Table 1 in v9.1) ---
    print("\n" + "-"*30 + " Final Max Search Depth Comparison " + "-"*30)
    print(f"  System A (S_n System r_max):                 {max_r_s_n}")
    print(f"  System B (Random Mod 30 c_max):            ~ {max_c_mod30}") # Note the '~' as it fluctuates
    print(f"  System C (Perfected Mod 210 r_max):          {max_r_mod210}")

    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION (Matches v9.1 Paper) " + "="*20)
    if max_r_mod210 < max_r_s_n and max_r_mod210 < max_c_mod30:
        print("\n  [VERDICT: The 'Perfected Mod 210' system is definitively superior.]")
        print("  It is superior in both instant fix rate and overall r_max.")
        print("  This proves the S_n system's efficiency is not unique,")
        print("  and that a stronger 'Primorial Filter' is the optimal path.")
    elif max_r_s_n <= max_r_mod210 and max_r_s_n <= max_c_mod30:
        print("\n  [VERDICT: The S_n sequence's 'natural' spacing remains competitive.]")
        print("  While Mod 210 has a higher instant fix rate, the S_n system's")
        print("  overall r_max is still the best or equal to the best found.")
        print("  This suggests a unique optimization in the S_n spacing.")
    else:
        print("\n  [VERDICT: Efficiency hierarchy confirmed. Primorial filter is key.]")
        print("  The results confirm the general trend: stronger filters are more efficient.")
        print("  The S_n system performs at roughly a Mod 30 level.")


    print("=" * (50 + len(" FINAL CONCLUSION (Matches v9.1 Paper) ")))


if __name__ == "__main__":
    run_comprehensive_showdown()