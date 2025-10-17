# ==============================================================================
# STEP 2: HEURISTIC ANALYSIS (The Fast, Analysis Step) - WITH DENSITY DEFENSE
# This script loads the pre-computed primes and runs the full heuristic analysis,
# then performs the targeted Density-Invariance Test (Defense 1).
# ==============================================================================

import math
import time
import random

# --- Configuration (Must match File 1) ---
INPUT_FILENAME = "primes_4m.txt" # This must be changed to "primes_4m.txt" to load the correct file
NUM_ANCHOR_POINTS = 4000000
PRIME_SEARCH_SAFETY_LIMIT = 500 
MAX_CORRECTION_RADIUS = 15 

# --- External Data Points for Density Test (Defense 1) ---
# We are testing the region near the largest gap (g_n=210).
# The prime 20,831,323 is close to this maximal stress point.
STARTING_PRIME_VALUE = 20831323 
CHECK_PAIRS = 20 # Number of prime pairs to check around the max gap location.
PROGRESS_INTERVAL = 100000 # Update progress every 100,000 pairs

# --- Utility Functions (Keep your original functions) ---

def load_primes_from_file(filename):
    """Loads primes efficiently from the generated file, and truncates the list."""
    print(f"Loading primes from {filename}...")
    start_time = time.time()
    
    with open(filename, 'r') as f:
        prime_list = [int(line.strip()) for line in f if line.strip()]
        
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} total primes in {end_time - start_time:.2f} seconds.")

    # Truncate the list to match the analytical size plus a small buffer.
    # The actual structural pairs verified are 2,000,000. We need 2,000,001 primes for the main loop.
    # We will use the size that defined the structural test environment.
    ANALYTICAL_PRIME_COUNT = NUM_ANCHOR_POINTS + MAX_CORRECTION_RADIUS + 2 

    if len(prime_list) > ANALYTICAL_PRIME_COUNT:
        # We discard the excess primes (the 1 million extra buffer)
        prime_list = prime_list[:ANALYTICAL_PRIME_COUNT]
        print(f"Truncated list for analysis: Using {len(prime_list):,} primes.")

    return prime_list

def sieve_up_to_r(limit):
    """Generates primes up to a small R_max limit for P_Expected calculation."""
    limit = int(limit)
    if limit < 2: return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for p in range(2, limit + 1):
        if is_prime[p]:
            for multiple in range(p*p, limit + 1, p):
                is_prime[multiple] = False
                
    return [p for p, is_p in enumerate(is_prime) if is_p]

# --- Core Analysis Logic ---

def find_correction_radius(p_list, p_set, anchor_index, max_r):
    """Performs Law I & Law III check for a single Anchor Point (used for defense)."""
    
    p_n = p_list[anchor_index]
    p_n_plus_1 = p_list[anchor_index + 1]
    anchor_sum = p_n + p_n_plus_1
    
    # 1. Find Closest Prime (q_closest) and k_min
    k_min = 0
    q_closest = 0 
    d = 1
    
    while True:
        found_lower = (anchor_sum - d)
        found_upper = (anchor_sum + d)
        
        if found_lower in p_set:
            k_min = d
            q_closest = found_lower
            break
        
        if found_upper in p_set:
            k_min = d
            q_closest = found_upper
            break
        
        # Safety break if search goes too deep (should not happen in this range)
        if d > PRIME_SEARCH_SAFETY_LIMIT: return {"k": 0, "r": 0, "gap": p_n_plus_1 - p_n, "status": "FAIL: Too far"}
        d += 1

    # Check Law I Result
    is_k_composite = (k_min > 1) and (k_min not in p_set)
    gap = p_n_plus_1 - p_n

    if not is_k_composite:
        return {"k": k_min, "r": 0, "gap": gap, "status": "SUCCESS: Law I Held"}

    # 2. Law III Correction Check (Only invoked if k is composite)
    target_prime = q_closest
    
    for radius in range(1, max_r + 1):
        
        # Check previous anchor (S_{n-r})
        idx_prev = anchor_index - radius
        if idx_prev >= 1: 
            s_prev = p_list[idx_prev] + p_list[idx_prev + 1]
            k_prev = abs(s_prev - target_prime) 
            if k_prev == 1 or k_prev in p_set:
                return {"k": k_min, "r": radius, "gap": gap, "status": f"CORRECTED by S_n-{radius}"}
        
        # Check next anchor (S_{n+r})
        idx_next = anchor_index + radius
        if idx_next + 1 < len(p_list):
            s_next = p_list[idx_next] + p_list[idx_next + 1]
            k_next = abs(s_next - target_prime) 
            if k_next == 1 or k_next in p_set:
                return {"k": k_min, "r": radius, "gap": gap, "status": f"CORRECTED by S_n+{radius}"}
    
    # 3. Law III Failure
    return {"k": k_min, "r": max_r, "gap": gap, "status": "FAILURE: Max Radius Exceeded"}


def run_density_invariance_check(p_list, p_set):
    """Performs Defense 1: Checks Anchor Points near the largest prime gap."""
    
    # Find the starting index near the maximal gap value
    start_index = 0
    for i, p in enumerate(p_list):
        if p >= STARTING_PRIME_VALUE:
            start_index = i
            break
            
    if start_index == 0:
        print("\n[Defense 1 Warning]: Could not find the large gap starting prime in the list.")
        return

    print("\n" + "="*80)
    print(f"DEFENSE 1: TESTING LAW III NEAR MAX STRESS ZONE (Gap={210} region)")
    print(f"Starting analysis near prime {p_list[start_index]:,}")
    print("-" * 80)
    print(f"{'Index':<6} | {'P_n':<12} | {'Gap':<5} | {'k_min':<5} | {'R_used':<6} | {'Status'}")
    print("-" * 80)

    max_r_found = 0
    
    # Iterate through the pairs immediately following the large gap location
    for i in range(start_index, start_index + CHECK_PAIRS):
        if i + 1 >= len(p_list): break
        
        p_n = p_list[i]
        result = find_correction_radius(p_list, p_set, i, MAX_CORRECTION_RADIUS)
        
        if result['status'] == "FAIL: Too far": continue

        # Check for the largest r needed
        if result['r'] > 0 and result['r'] > max_r_found:
            max_r_found = result['r']
        
        # Print results for every pair in the stress zone
        print(f"{i:<6} | {p_n:<12,} | {result['gap']:<5} | {result['k']:<5} | {result['r']:<6} | {result['status']}")

    print("-" * 80)
    print(f"Defense Summary: Max correction radius required in this stressed region was r={max_r_found}")
    print("="*80)


def run_heuristic_analysis():
    """
    Calculates P_Observed (from true Anchors) and a new, more accurate
    P'_Baseline (from a random control group) to find the true bias.
    """
    
    all_primes = load_primes_from_file(INPUT_FILENAME)
    
    # We can only test N-1 pairs if we have N primes available for pairing.
    # So we adjust the number of anchor points to test.
    NUM_ANCHOR_POINTS_TO_TEST = len(all_primes) - 2 # This will be 3,999,999

    if len(all_primes) < NUM_ANCHOR_POINTS + 1:
        print(f"Error: Not enough primes loaded. Check {INPUT_FILENAME} integrity.")
        return

    prime_set = set(all_primes) # For fast O(1) lookups
    
    # ==========================================================================
    # --- Part 1: Empirical Test (P_Observed using TRUE Anchors) ---
    # ==========================================================================
    print(f"\nStarting primary loop over {NUM_ANCHOR_POINTS_TO_TEST:,} TRUE Anchor Points...")
    primary_loop_start_time = time.time()
    
    clean_k_count_observed = 0
    max_k_min = 0 

    # --- Adjusted the loop range here ---
    for i in range(1, NUM_ANCHOR_POINTS_TO_TEST + 1): 
        if i % PROGRESS_INTERVAL == 0:
            print(f"PROGRESS (True Anchors): {i:,} / {NUM_ANCHOR_POINTS_TO_TEST:,} processed", end='\r', flush=True)

        p_n = all_primes[i]
        p_n_plus_1 = all_primes[i+1] 
        s_n = p_n + p_n_plus_1

        k_min = 0
        search_radius = 1
        while search_radius <= PRIME_SEARCH_SAFETY_LIMIT: 
            if ((s_n - search_radius) in prime_set) or ((s_n + search_radius) in prime_set):
                k_min = search_radius
                break
            search_radius += 1

        if (k_min == 1) or (k_min > 1 and k_min in prime_set):
            clean_k_count_observed += 1
        
        if k_min > max_k_min:
            max_k_min = k_min

    print(f"PROGRESS (True Anchors): {NUM_ANCHOR_POINTS_TO_TEST:,} / {NUM_ANCHOR_POINTS_TO_TEST:,} processed. Complete.     ")
    p_observed = clean_k_count_observed / NUM_ANCHOR_POINTS_TO_TEST
    
    # ==========================================================================
    # --- Part 2: Control Test (P'_Baseline using RANDOM Anchors) ---
    # ==========================================================================
    print(f"\nStarting control loop over {NUM_ANCHOR_POINTS_TO_TEST:,} RANDOM Anchor Points...")
    control_loop_start_time = time.time()
    
    clean_k_count_control = 0
    
    # --- Adjusted the loop range here as well ---
    for i in range(1, NUM_ANCHOR_POINTS_TO_TEST + 1):
        if i % PROGRESS_INTERVAL == 0:
            print(f"PROGRESS (Random Anchors): {i:,} / {NUM_ANCHOR_POINTS_TO_TEST:,} processed", end='\r', flush=True)

        p_n = all_primes[i]
        p_n_plus_1 = all_primes[i+1]
        s_n_magnitude = p_n + p_n_plus_1
        
        lower_bound = int(s_n_magnitude * 0.9)
        upper_bound = int(s_n_magnitude * 1.1)
        random_num = random.randint(lower_bound, upper_bound)
        s_control = random_num if random_num % 2 == 0 else random_num + 1

        k_min = 0
        search_radius = 1
        while search_radius <= PRIME_SEARCH_SAFETY_LIMIT:
            q_lower = s_control - search_radius
            if (q_lower > 1 and q_lower in prime_set) or ((s_control + search_radius) in prime_set):
                k_min = search_radius
                break
            search_radius += 1
        
        if (k_min == 1) or (k_min > 1 and k_min in prime_set):
            clean_k_count_control += 1

    print(f"PROGRESS (Random Anchors): {NUM_ANCHOR_POINTS_TO_TEST:,} / {NUM_ANCHOR_POINTS_TO_TEST:,} processed. Complete.    ")
    p_baseline_control = clean_k_count_control / NUM_ANCHOR_POINTS_TO_TEST

    # ==========================================================================
    # --- Part 3: Final Analysis & Comparison ---
    # ==========================================================================
    
    print("\n" + "="*70)
    print("        NULL HYPOTHESIS TEST: BIAS CONFIRMATION ANALYSIS      ")
    print("="*70)
    print(f"Total Analysis Time: {time.time() - primary_loop_start_time:.2f} seconds")
    print("-" * 70)
    print(f"P_Observed (True Prime Anchors): {p_observed:.4f} ({p_observed * 100:.2f}%)")
    print(f"P'_Baseline (Random Control Group): {p_baseline_control:.4f} ({p_baseline_control * 100:.2f}%)")
    
    true_bias = p_observed - p_baseline_control
    
    if true_bias > 0.005: 
        print(f"\n** BIAS CONFIRMED: {true_bias * 100:.2f} percentage points HIGHER than control baseline. **")
    else:
        print(f"\n** BIAS NOT CONFIRMED: Result is not significantly different from the control baseline. **")
    print("="*70)

    # --- Part 4: Run Density Invariance Check (this remains the same) ---
    run_density_invariance_check(all_primes, prime_set)


if __name__ == "__main__":
    run_heuristic_analysis()
