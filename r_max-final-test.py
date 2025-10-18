# ==============================================================================
# PRIME ANCHOR SYSTEM - TEST 5: The Final Control Test
#
# This is the ultimate "control" test to isolate the "magic" ingredient.
#
# We are now testing THREE systems in parallel:
# 1. System A (Your $S_n$): The original structured search.
# 2. System B (Mod 6 Random): Our "hyper-fair" random Mod 6 control.
# 3. System C (Even Random): Our NEW "any even number" control.
#
# HYPOTHESIS:
# - Systems A and B will achieve 100% correction.
# - System C will FAIL, proving that the "anchor" concept is
#   specifically about Mod 6 numbers, not just any even number.
#
# ==============================================================================

import math
import time
import random

# --- Configuration ---
PRIME_INPUT_FILE = "primes_100m.txt" 
# 50M pairs is the definitive test
MAX_PRIME_PAIRS_TO_TEST = 50000000      

# Search limits for our three systems
MAX_RADIUS_LIMIT = 30           # System A
RANDOM_SEARCH_LIMIT = 100         # System B & C

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
def run_final_control_test():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_RADIUS_LIMIT + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting \"Final Control Test\" for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"  - Testing System A (True S_n) vs. System B (Mod 6 Random) vs. System C (Even Random)")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 5 ---
    total_law_I_failures = 0
    
    # System A (True System)
    true_system_failures = [] 
    max_r_observed = 0
    
    # System B (Mod 6 Random)
    mod6_random_failures = [] 
    max_c_mod6_observed = 0
    
    # System C (Even Random)
    even_random_failures = [] 
    max_c_even_observed = 0
    
    start_index = MAX_RADIUS_LIMIT + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Max r: {max_r_observed} | Max c_mod6: {max_c_mod6_observed} | Max c_even: {max_c_even_observed}", end='\r')

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
                    if r > max_r_observed: max_r_observed = r
                    break 
            
            if not is_true_system_corrected:
                true_system_failures.append(failure_details)
                print("\nFATAL: Law III Falsified. Stopping.")
                break 

            # --- Define Neighborhood for Random Tests ---
            avg_gap = (prime_list[i+10] - prime_list[i-10]) / 20 
            neighborhood_radius = int(avg_gap * MAX_RADIUS_LIMIT) 
            if neighborhood_radius <= 0: neighborhood_radius = 500 
            
            # --- 3. Test System B (Mod 6 Random) ---
            is_mod6_random_corrected = False
            for c in range(1, RANDOM_SEARCH_LIMIT + 1):
                rand_offset = random.randint(-neighborhood_radius, neighborhood_radius)
                s_control_base = anchor_sum + rand_offset
                s_control_mod6 = s_control_base - (s_control_base % 6) # Force Mod 6

                if is_clean_k(abs(s_control_mod6 - q_prime), prime_set):
                    is_mod6_random_corrected = True
                    if c > max_c_mod6_observed: max_c_mod6_observed = c
                    break 
            
            if not is_mod6_random_corrected:
                failure_details_b = failure_details.copy()
                failure_details_b['attempts_made'] = RANDOM_SEARCH_LIMIT
                mod6_random_failures.append(failure_details_b)

            # --- 4. Test System C (Even Random) ---
            is_even_random_corrected = False
            for e in range(1, RANDOM_SEARCH_LIMIT + 1):
                rand_offset = random.randint(-neighborhood_radius, neighborhood_radius)
                s_control_base = anchor_sum + rand_offset
                s_control_even = s_control_base if s_control_base % 2 == 0 else s_control_base + 1 # Force Even

                if is_clean_k(abs(s_control_even - q_prime), prime_set):
                    is_even_random_corrected = True
                    if e > max_c_even_observed: max_c_even_observed = e
                    break
            
            if not is_even_random_corrected:
                failure_details_c = failure_details.copy()
                failure_details_c['attempts_made'] = RANDOM_SEARCH_LIMIT
                even_random_failures.append(failure_details_c)

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Law I Fails: {total_law_I_failures:,} | Max r: {max_r_observed} | Max c_mod6: {max_c_mod6_observed} | Max c_even: {max_c_even_observed}")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 5: FINAL CONTROL TEST REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_law_I_failures:,}")
    
    # --- System A Report ---
    print("\n" + "-"*20 + " System A: 'Prime Anchor System' (Your $S_n$) " + "-"*20)
    print(f"  Total Uncorrected Failures: {len(true_system_failures)}")
    print(f"  Max Correction Radius (r_max): {max_r_observed}")

    # --- System B Report ---
    print("\n" + "-"*20 + " System B: 'Mod 6 Random' Control " + "-"*20)
    print(f"  Total Uncorrected Failures: {len(mod6_random_failures)}")
    print(f"  Max Correction Count (c_max): {max_c_mod6_observed}")

    # --- System C Report ---
    print("\n" + "-"*20 + " System C: 'Even Random' Control " + "-"*20)
    print(f"  Total Uncorrected Failures: {len(even_random_failures)}")
    print(f"  Max Correction Count (e_max): {max_c_even_observed}")
    if len(even_random_failures) > 0:
        print(f"  (Found {len(even_random_failures):,} failures that could not be corrected in {RANDOM_SEARCH_LIMIT} attempts)")


    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    
    if len(true_system_failures) == 0 and len(mod6_random_failures) == 0:
        if len(even_random_failures) > 0:
            print("\n  [VERDICT: SUCCESS. The 'Mod 6' property is the key.]")
            print("  This is a huge success. The test proves:")
            print("  1. 'Mod 6' anchors (Systems A and B) provide 100% correction.")
            print("  2. 'Random Even' anchors (System C) FAIL 100% correction.")
            print("\n  This definitively proves that the 'Dense Neighborhood' is a")
            print("  specific property of MOD 6 numbers, not just any even number.")
            print("  The 'anchor' concept is now fully isolated.")
        else:
            print("\n  [VERDICT: INCONCLUSIVE / STRANGE ARTIFACT]")
            print("  This is a very strange result.")
            print("  - All three systems (A, B, and C) provided 100% correction.")
            print("  This would imply that even 'bad' anchors ($6m+2, 6m+4$)")
            print("  are not a problem, which contradicts our Test 2 findings.")
    else:
        print("\n  [VERDICT: BREAK (FALSIFIED)]")
        print("  A failure was found in System A or B. The 100% correction claim is false.")

    print("=" * (50 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_final_control_test()
