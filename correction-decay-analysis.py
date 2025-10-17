# ==============================================================================
# Deterministic Decay Analysis
#
# Law III correction mechanism over discrete intervals, allowing for a
# quantitative analysis of the "deterministic decay."
# ==============================================================================

import math
import time

# --- Configuration ---
# -- Generate Prime sets first using generate-primes.py --
PRIME_INPUT_FILE = "primes_100m.txt"
MAX_PRIME_PAIRS_TO_TEST = 50000000
MAX_CORRECTION_RADIUS = 20
DECAY_ANALYSIS_INTERVAL = 100000 # Analyze the decay every 100,000 pairs

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

# --- Main Testing Logic ---
def test_correction_law():
    """Tests Law III and analyzes the stability of its deterministic decay."""
    
    prime_list = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    required_primes_count = MAX_PRIME_PAIRS_TO_TEST + MAX_CORRECTION_RADIUS + 2
    if len(prime_list) < required_primes_count:
        print("\nFATAL ERROR: The loaded prime file is too small for this test.")
        # ... (error reporting)
        return

    print("\nSafety check passed. Creating prime set for fast lookups...")
    prime_set = set(prime_list)
    print("Prime set created. Starting analysis...")
    print("-" * 80)
    start_time = time.time()
    
    # --- Data structures for the new decay analysis ---
    decay_stats = {}
    interval_exceptions = 0
    interval_corrections = {}

    # --- Data structures for the main report ---
    total_successful_corrections = {}
    correction_failures = []
    max_r_observed = 0

    start_index = MAX_CORRECTION_RADIUS + 1
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        
        # --- Standard Progress Tracker ---
        if i % DECAY_ANALYSIS_INTERVAL == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Max r: {max_r_observed} | Time: {elapsed:.0f}s", end='\r')
            
            # --- Store results for the completed interval ---
            if interval_exceptions > 0:
                decay_stats[i] = {
                    'exceptions': interval_exceptions,
                    'corrections': interval_corrections.copy()
                }
            # --- Reset counters for the next interval ---
            interval_exceptions = 0
            interval_corrections.clear()

        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        min_distance_k = 0
        search_dist = 1
        while True:
            if (anchor_sum - search_dist) in prime_set or (anchor_sum + search_dist) in prime_set:
                min_distance_k = search_dist
                break
            search_dist += 1
        
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            interval_exceptions += 1 # Increment interval exception counter
            
            q_prime = 0
            if (anchor_sum - min_distance_k) in prime_set: q_prime = anchor_sum - min_distance_k
            else: q_prime = anchor_sum + min_distance_k
            
            is_corrected = False
            for radius in range(1, MAX_CORRECTION_RADIUS + 1):
                # (Correction logic is the same as before)
                s_prev = prime_list[i - radius] + prime_list[i - radius + 1]
                if abs(s_prev - q_prime) == 1 or abs(s_prev - q_prime) in prime_set: is_corrected = True
                if not is_corrected:
                    s_next = prime_list[i + radius] + prime_list[i + radius + 1]
                    if abs(s_next - q_prime) == 1 or abs(s_next - q_prime) in prime_set: is_corrected = True

                if is_corrected:
                    # Update both total and interval stats
                    total_successful_corrections[radius] = total_successful_corrections.get(radius, 0) + 1
                    interval_corrections[radius] = interval_corrections.get(radius, 0) + 1
                    if radius > max_r_observed: max_r_observed = radius
                    break
            
            if not is_corrected:
                correction_failures.append({"original_anchor": anchor_sum, "prime_q": q_prime, "composite_k": min_distance_k})
                break

    print(f"Progress: {MAX_PRIME_PAIRS_TO_TEST:,} / {MAX_PRIME_PAIRS_TO_TEST:,} | Max r: {max_r_observed} | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")

    # ==========================================================================
    # --- DETERMINISTIC DECAY ANALYSIS REPORT ---
    # ==========================================================================
    print("\n\n" + "="*20 + " DETERMINISTIC DECAY STABILITY ANALYSIS " + "="*20)
    print("This report shows the percentage of exceptions corrected at a radius of r=1 and r=2 for each interval.")
    print("-" * 85)
    print(f"{'Pair Interval End':<20} | {'Total Exceptions':<20} | {'% Corrected @ r=1':<20} | {'% Corrected @ r<=2'}")
    print("-" * 85)

    cumulative_r1_total = 0
    cumulative_r2_total = 0
    cumulative_exceptions_total = 0

    for interval_end, stats in decay_stats.items():
        exceptions_count = stats['exceptions']
        if exceptions_count == 0: continue

        r1_count = stats['corrections'].get(1, 0)
        r2_count = stats['corrections'].get(2, 0)
        
        cumulative_r1_total += r1_count
        cumulative_r2_total += r1_count + r2_count
        cumulative_exceptions_total += exceptions_count

        r1_percent = (r1_count / exceptions_count) * 100
        cumulative_r2_percent = ((r1_count + r2_count) / exceptions_count) * 100
        
        print(f"{interval_end:<20,} | {exceptions_count:<20,} | {r1_percent:<20.2f}% | {cumulative_r2_percent:.2f}%")

    # --- Final average calculation ---
    if cumulative_exceptions_total > 0:
        avg_r1_percent = (cumulative_r1_total / cumulative_exceptions_total) * 100
        avg_cumulative_r2_percent = (cumulative_r2_total / cumulative_exceptions_total) * 100
        print("-" * 85)
        print(f"{'OVERALL AVERAGE':<20} | {cumulative_exceptions_total:<20,} | {avg_r1_percent:<20.2f}% | {avg_cumulative_r2_percent:.2f}%")
        print("-" * 85)

if __name__ == "__main__":
    test_correction_law()
