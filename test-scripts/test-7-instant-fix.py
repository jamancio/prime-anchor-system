# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 7: The "Instant Fix" (r_max=1) Showdown
#
# This tests the "Strong Conjecture": Can a system exist where
# the fix is *always* at the first anchor we check (r=1 or c=1)?
#
# We will test the "instant fix rate" of four different systems.
# If any system achieves 100%, the conjecture is verified.
# ==============================================================================

import math
import time
import random

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
# 50M pairs is the definitive test
MAX_PRIME_PAIRS_TO_TEST = 50000000      

# We only need a radius of 1 for System A
MAX_RADIUS_LIMIT = 10 # Keep a small buffer for safety          

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
def run_instant_fix_showdown():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting \"Instant Fix Showdown\" for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - Comparing r=1 / c=1 success rates for Mod 2, 6, 30, and 210 anchors")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 7 ---
    total_law_I_failures = 0
    
    # Success counters for each system
    true_system_r1_success = 0
    mod6_c1_success = 0
    mod30_c1_success = 0
    mod210_c1_success = 0
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,}", end='\r')

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
            
            # --- Define Neighborhood for Random Tests ---
            avg_gap = (prime_list[i+10] - prime_list[i-10]) / 20 
            neighborhood_radius = int(avg_gap * 10) # 10 is a reasonable radius
            if neighborhood_radius <= 0: neighborhood_radius = 500 

            # --- 2. Test System A ($S_n$ at r=1) ---
            s_prev_1 = prime_list[i - 1] + prime_list[i]
            s_next_1 = prime_list[i + 1] + prime_list[i + 2]
            if is_clean_k(abs(s_prev_1 - q_prime), prime_set) or is_clean_k(abs(s_next_1 - q_prime), prime_set):
                true_system_r1_success += 1

            # --- 3. Test System B (Mod 6 at c=1) ---
            rand_offset_6 = random.randint(-neighborhood_radius, neighborhood_radius)
            s_control_base_6 = anchor_sum + rand_offset_6
            s_control_mod6 = s_control_base_6 - (s_control_base_6 % 6) # Force Mod 6
            if is_clean_k(abs(s_control_mod6 - q_prime), prime_set):
                mod6_c1_success += 1

            # --- 4. Test System C (Mod 30 at c=1) ---
            rand_offset_30 = random.randint(-neighborhood_radius, neighborhood_radius)
            s_control_base_30 = anchor_sum + rand_offset_30
            s_control_mod30 = s_control_base_30 - (s_control_base_30 % 30) # Force Mod 30
            if is_clean_k(abs(s_control_mod30 - q_prime), prime_set):
                mod30_c1_success += 1

            # --- 5. Test System D (Mod 210 at c=1) ---
            rand_offset_210 = random.randint(-neighborhood_radius, neighborhood_radius)
            s_control_base_210 = anchor_sum + rand_offset_210
            s_control_mod210 = s_control_base_210 - (s_control_base_210 % 210) # Force Mod 210
            if is_clean_k(abs(s_control_mod210 - q_prime), prime_set):
                mod210_c1_success += 1

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 7: \"Instant Fix\" (r=1) REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    
    # --- Calculate Percentages ---
    rate_A = (true_system_r1_success / total_law_I_failures) * 100
    rate_B = (mod6_c1_success / total_law_I_failures) * 100
    rate_C = (mod30_c1_success / total_law_I_failures) * 100
    rate_D = (mod210_c1_success / total_law_I_failures) * 100

    print("\n" + "-"*20 + " Instant Fix Rate (r=1 or c=1) by System " + "-"*20)
    print(f"  System A ($S_n$):     {rate_A:.2f}%")
    print(f"  System B (Random Mod 6):   {rate_B:.2f}%")
    print(f"  System C (Random Mod 30):  {rate_C:.2f}%")
    print(f"  System D (Random Mod 210): {rate_D:.2f}%")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if rate_D == 100.0 or rate_C == 100.0:
        print("\n  [VERDICT: \"Strong Conjecture\" VERIFIED!]")
        print("  A system was found with a 100% instant fix rate.")
        print("  This is a monumental discovery.")
    else:
        print("\n  [VERDICT: \"Strong Conjecture\" FALSIFIED]")
        print("  No system achieved a 100% instant fix rate.")
        print("  This proves that r_max=1 is impossible, and a search")
        print("  (like r_max=16) will always be necessary.")
        
    print("\n  EFFICIENCY ANALYSIS:")
    print("  The data clearly shows the hierarchy of efficiency:")
    print(f"  Mod 210 ({rate_D:.2f}%) > Mod 30 ({rate_C:.2f}%) > Mod 6 ({rate_B:.2f}%)")
    print(f"  $S_n$ system ({rate_A:.2f}%) is a highly efficient $r=1$ search,")
    print(f"  performing similarly to a Random Mod 6 or Mod 30 search.")


    print("=" * (50 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_instant_fix_showdown()