# ==============================================================================
# PAS LAW III ANALYSIS - TEST 1: r_max for the Optimal Filter (r_min Conjecture)
#
# NEW RESEARCH FRONTIER: UNIVERSALIZING THE PLR THEOREM
#
# This test applies the PLR's structural insight to the PAS problem.
#
# GOAL:
# Measure the maximum correction radius (r_max) for the most efficient
# Primorial Anchor: Anchor S_n' where S_n' == 0 (mod 210).
#
# This test confirms the physical stability of the structure underlying the PLR
# and determines if r_max = 10 is the final r_min constant.
# ==============================================================================

import time
import math
import json
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "prime/primes_100m.txt"
PRIMES_TO_TEST = 50000000
START_INDEX = 10
MAX_LAW_III_RADIUS = 25 # Max radius to search (must be larger than the known max of 16/10)

# --- Function to load primes from a file ---
def load_primes_from_file(filename):
    """Loads ALL primes and the set for lookups."""
    print(f"Loading ALL primes from {filename}...")
    start_time = time.time()
    try:
        with open(filename, 'r') as f:
            prime_list = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        return None, None
    
    prime_set = set(prime_list)
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes and set in {end_time - start_time:.2f} seconds.")
    
    required_primes = PRIMES_TO_TEST + START_INDEX + MAX_LAW_III_RADIUS + 2
    if len(prime_list) < required_primes:
        print(f"\nFATAL ERROR: Prime file is too small for this test.")
        return None, None
        
    return prime_list, prime_set

def is_prime(k_val, prime_set):
    """Helper function to check if k is prime."""
    if k_val < 2: return False
    return k_val in prime_set

def is_clean_k(k_val, prime_set):
    """Defines a 'Clean' distance k (k=1 or k is prime)."""
    if k_val == 1: return True
    if k_val < 2: return False
    return is_prime(k_val, prime_set)
    
def get_k_min(anchor_sn, prime_set):
    """Finds the k_min for a given anchor."""
    min_distance_k = 0
    search_dist = 1
    while True:
        q_lower = anchor_sn - search_dist
        q_upper = anchor_sn + search_dist
        if q_lower in prime_set: min_distance_k = search_dist; break
        if q_upper in prime_set: min_distance_k = search_dist; break
        search_dist += 1
        if search_dist > 2000: return -1 # Failsafe for maximal gaps
    return min_distance_k
    
# --- Main Testing Logic ---
def run_pas_rmax_test():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PAS Law III r_max Test (Test 1) for {PRIMES_TO_TEST:,} primes...")
    print(f"  - System: Optimal Mod 210 Anchor System")
    print(f"  - Max Search Depth: {MAX_LAW_III_RADIUS}")
    print("-" * 80)
    start_time = time.time()
    
    total_anchors_tested = 0
    total_law_I_failures = 0
    
    # --- Structural Data ---
    max_r_observed = 0
    unresolved_failures = 0
    resolved_failures = 0

    # Start loop slightly later to allow for the r_max search range backward
    loop_start_index = START_INDEX + MAX_LAW_III_RADIUS 
    loop_end_index = PRIMES_TO_TEST + loop_start_index
    
    if loop_end_index >= len(prime_list) - MAX_LAW_III_RADIUS - 1:
        print(f"\nFATAL ERROR: Not enough primes loaded for S_n+r lookups at the end.")
        return

    for i in range(loop_start_index, loop_end_index):
        if (i - loop_start_index + 1) % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - loop_start_index + 1
            print(f"Progress: {progress:,} / {PRIMES_TO_TEST:,} | Failures: {total_law_I_failures:,} | r_max: {max_r_observed} | Time: {elapsed:.0f}s", end='\r')

        # We are only interested in the most efficient anchors: Anchor S_n' == 0 (mod 210)
        # We check every anchor, but only log if it's a multiple of 210.
        
        anchor_S_n = prime_list[i] + prime_list[i + 1]
        
        # --- 1. Identify Anchor of Interest ---
        if anchor_S_n % 210 != 0:
            continue
            
        total_anchors_tested += 1
        
        # --- 2. Check Law I Status ---
        k_min = get_k_min(anchor_S_n, prime_set)
        
        is_k_composite = (k_min > 1) and not is_prime(k_min, prime_set)
        
        if is_k_composite:
            # Law I Failure: This anchor is "messy." We must find the fix.
            total_law_I_failures += 1
            
            # --- 3. Perform Law III Search ---
            
            # The prime that caused the composite k_min (q_closest)
            q_closest_lower = anchor_S_n - k_min
            q_closest_upper = anchor_S_n + k_min
            
            q_closest = 0
            if q_closest_lower in prime_set: q_closest = q_closest_lower
            elif q_closest_upper in prime_set: q_closest = q_closest_upper
            
            if q_closest == 0: continue # Skip if closest prime couldn't be found (e.g., k_min > 2000)

            r_fix = -1 
            
            # Search from r=1 outwards to find the fix
            for r in range(1, MAX_LAW_III_RADIUS + 1):
                # Check S_{n-r}
                S_prev = prime_list[i - r] + prime_list[i - r + 1]
                # Check S_{n+r}
                S_next = prime_list[i + r] + prime_list[i + r + 1]
                
                # The correction is found if the distance from S_prev/S_next to q_closest is "clean"
                if is_clean_k(abs(S_prev - q_closest), prime_set) or is_clean_k(abs(S_next - q_closest), prime_set):
                    r_fix = r
                    max_r_observed = max(max_r_observed, r)
                    resolved_failures += 1
                    break
            
            if r_fix == -1:
                unresolved_failures += 1

    # --- Final Summary ---
    progress = total_anchors_tested
    print(f"Progress: {progress:,} anchors tested | Failures: {total_law_I_failures:,} | Max r: {max_r_observed} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    print("\n" + "="*20 + " PAS Law III r_max Test (Test 1) Report " + "="*20)
    print(f"\nTotal Optimal Anchors Tested (S_n == 0 mod 210): {total_anchors_tested:,}")
    print(f"Total Law I Failures Found: {total_law_I_failures:,}")
    
    
    failure_rate = (total_law_I_failures / total_anchors_tested) * 100 if total_anchors_tested > 0 else 0
    resolution_rate = (resolved_failures / total_law_I_failures) * 100 if total_law_I_failures > 0 else 0
    
    print("\n" + "-" * 20 + " Final Structural Metrics " + "-" * 20)
    print(f"  Law I Failure Rate (Initial Messiness): {failure_rate:.4f}%")
    print(f"  Max Correction Radius (r_max):          {max_r_observed}")
    print(f"  Total Unresolved Failures:              {unresolved_failures:,}")
    print(f"  Final Resolution Rate:                  {resolution_rate:.2f}%")
    
    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL ANALYTIC CONCLUSION " + "="*20)
    
    if resolution_rate == 100.0:
        if max_r_observed < 10:
            print(f"\n  [VERDICT: R_MIN CONJECTURE SOLVED (r_max = {max_r_observed} < 10)]")
            print("  The theoretical minimum correction radius is smaller than anticipated.")
        elif max_r_observed == 10:
            print(f"\n  [VERDICT: R_MIN CONJECTURE CONFIRMED (r_max = 10)]")
            print("  The theoretical minimum correction radius is confirmed to be 10.")
        else:
            print(f"\n  [VERDICT: STRUCTURAL PROBLEM IS HARDER (r_max = {max_r_observed})]")
            print("  The structural problem is harder than originally measured.")
    else:
        print("\n  [VERDICT: LAW III FALSIFIED/INCOMPLETE DATA]")
        print("  The 100% self-correction property (Law III) has failed.")

    print("=" * (50 + len(" FINAL ANALYTIC CONCLUSION ")))

if __name__ == "__main__":
    run_pas_rmax_test()