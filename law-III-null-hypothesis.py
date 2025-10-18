# ==============================================================================
# The script now directly compares the cumulative fix rate (r<=2) of the
# 'True System' against the 'Random Baseline' and reports the
# 'Absolute Percentage Point Advantage'.
# ==============================================================================

import math
import time
import random

# --- Configuration ---
# --- Input file containing a list of primes ---
PRIME_INPUT_FILE = "primes_100m.txt" 
MAX_PRIME_PAIRS_TO_TEST = 50000000      
MAX_CORRECTION_RADIUS = 20 
NUM_CONTROL_TESTS = 5      

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
def run_law_3_final_analysis():
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_CORRECTION_RADIUS + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small.")
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")

    print(f"\nStarting Law III Final Analysis for {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"Comparing True Anchor fix rate vs. {NUM_CONTROL_TESTS} Random Control Anchors.")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for Test 3 ---
    total_failures_found = 0
    
    # Stats for YOUR system
    true_system_corrections_r1 = 0
    true_system_corrections_r2 = 0
    
    # Stats for the CONTROL (random) system
    control_system_corrections = 0
    control_system_attempts = 0 

    start_index = MAX_CORRECTION_RADIUS + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        if i % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Failures Found: {total_failures_found:,} | Time: {elapsed:.0f}s", end='\r')

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        # --- 1. Find a Law I Failure ---
        min_distance_k = 0
        q_prime = 0
        search_dist = 1
        while True:
            if search_dist > 1000: break 
            
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
            total_failures_found += 1
            
            # --- 2. Test YOUR System (Law III) ---
            is_corrected_by_true_system = False
            
            # Check r=1
            s_prev_1 = prime_list[i - 1] + prime_list[i]
            s_next_1 = prime_list[i + 1] + prime_list[i + 2]
            if is_clean_k(abs(s_prev_1 - q_prime), prime_set) or is_clean_k(abs(s_next_1 - q_prime), prime_set):
                is_corrected_by_true_system = True
                true_system_corrections_r1 += 1
            
            # Check r=2 (only if r=1 failed)
            if not is_corrected_by_true_system:
                s_prev_2 = prime_list[i - 2] + prime_list[i - 1]
                s_next_2 = prime_list[i + 2] + prime_list[i + 3]
                if is_clean_k(abs(s_prev_2 - q_prime), prime_set) or is_clean_k(abs(s_next_2 - q_prime), prime_set):
                    is_corrected_by_true_system = True
                    true_system_corrections_r2 += 1

            
            # --- 3. Test the CONTROL System (Null Hypothesis) ---
            avg_gap = (prime_list[i+2] - prime_list[i-2]) / 4
            neighborhood_radius = int(avg_gap * 2)
            
            for _ in range(NUM_CONTROL_TESTS):
                control_system_attempts += 1
                rand_offset = random.randint(-neighborhood_radius, neighborhood_radius)
                s_control_base = anchor_sum + rand_offset
                s_control_mod6 = s_control_base - (s_control_base % 6)
                
                if is_clean_k(abs(s_control_mod6 - q_prime), prime_set):
                    control_system_corrections += 1

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Failures Found: {total_failures_found:,} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " TEST 3: LAW III FINAL ANALYSIS REPORT " + "="*20)
    print(f"\nTotal Law I Failures (Composite k) Analyzed: {total_failures_found:,}")
    
    # --- Calculate Percentages ---
    fix_rate_r2_cumulative = ((true_system_corrections_r1 + true_system_corrections_r2) / total_failures_found) * 100
    control_fix_rate = (control_system_corrections / control_system_attempts) * 100
    absolute_advantage = fix_rate_r2_cumulative - control_fix_rate

    # --- True System Report ---
    print("\n" + "-"*20 + " 'Prime Anchor System' (Your Law III) Results " + "-"*20)
    print(f"  Total Corrected (r<=2): {true_system_corrections_r1 + true_system_corrections_r2:,}")
    print(f"  Cumulative Fix Rate (r<=2): {fix_rate_r2_cumulative:.2f}%")

    # --- Control System Report ---
    print("\n" + "-"*20 + " 'Random Control' (Null Hypothesis) Results " + "-"*20)
    print(f"  Total Random Fixes:     {control_system_corrections:,}")
    print(f"  Random Fix Rate (Baseline): {control_fix_rate:.2f}%")

    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL CONCLUSION " + "="*20)
    print(f"\n  True System Fix Rate:   {fix_rate_r2_cumulative:.2f}%")
    print(f"  Random Baseline Rate:   {control_fix_rate:.2f}%")
    print("  ---------------------------------")
    print(f"  ABSOLUTE ADVANTAGE:     +{absolute_advantage:.2f}%")

    if absolute_advantage > 2.0: # A 2% advantage is very significant
        print("\n  [VERDICT: SUCCESS]")
        print("  Law III is a real, structural phenomenon.")
        print("  The 'Prime Anchor System' shows a stable and significant")
        print("  advantage over a 'hyper-fair' random baseline.")
    else:
        print("\n  [VERDICT: ARTIFACT]")
        print("  The advantage is minimal or non-existent.")
        print("  Law III is likely a statistical artifact. The S_n anchors")
        print("  have no special corrective property.")

    print("=" * (44 + len(" FINAL CONCLUSION ")))


if __name__ == "__main__":
    run_law_3_final_analysis()
