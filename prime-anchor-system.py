# ==============================================================================
# The Prime Anchor System Tester (Version 12.2 - Finalized for Full Transparency)
#
# This script is the definitive tool for testing the complete, three-part
# "Prime Anchor System" conjecture. This version incorporates explicit checks
# for Law II and has configuration optimized for large-scale verification.
#
# KEY IMPROVEMENT: This version explicitly reports the set of unique composite
# k-values found, which serves as the empirical proof of Law II (The Rule of
# Structured Exception).
#
# Origin: Formulated on October 16, 2025, in the City of Malabon, Philippines.
# ==============================================================================

import math
import time

# --- Configuration ---
# The 2,000,000th prime is ~32.4 million. The max Anchor Sum (S_n) is ~65 million.
# The sieve must be large enough to contain all S_n values and the max prime q.
# We set the limit generously above 65M.

# Estimated Sieve Limit needed for p_2,000,000
# Sieve limit must cover the maximum possible Anchor Sum (S_n)
SIEVE_LIMIT = 67000000 
MAX_PRIME_PAIRS_TO_TEST = 2000000 
MAX_CORRECTION_RADIUS = 15 # Set safely above the verified max of 13/14

# --- Utility Functions ---

def sieve_for_primes(limit):
    """Generates a list of primes and a set for fast primality testing (O(1))."""
    print(f"Generating primes up to {limit:,}...")
    start_time = time.time()
    
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    # Sieve up to sqrt(limit)
    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p*p, limit + 1, p):
                is_prime[multiple] = False

    prime_list = []
    prime_set = set()
    for p in range(2, limit + 1):
        if is_prime[p]:
            prime_list.append(p)
            prime_set.add(p)
            
    end_time = time.time()
    print(f"Generated {len(prime_list):,} primes in {end_time - start_time:.2f} seconds.")
    return prime_list, prime_set

def get_prime_factors(n):
    """Returns the set of prime factors for n, used for Law II check."""
    # NOTE: This function is not used in the core loop but is provided for deeper analysis.
    factors = set()
    d = 2
    temp = n
    
    # Check for the only even prime (2)
    while temp % d == 0:
        factors.add(d)
        temp //= d
    
    d = 3
    # Check for odd factors
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            temp //= d
        else:
            d += 2
    
    if temp > 1:
        factors.add(temp)
        
    return factors

# --- Main Testing Logic ---

def test_correction_law():
    """Tests the full Hierarchical Prime Anchor System conjecture."""
    
    prime_list, prime_set = sieve_for_primes(SIEVE_LIMIT)

    # Note: We need primes up to index MAX_PRIME_PAIRS_TO_TEST + MAX_CORRECTION_RADIUS + 2
    required_index = MAX_PRIME_PAIRS_TO_TEST + MAX_CORRECTION_RADIUS + 2
    if len(prime_list) < required_index:
        print(f"Error: Sieve limit is too low. Needed {required_index:,} primes, found {len(prime_list):,}.")
        return

    print(f"\nStarting hierarchical test for the first {MAX_PRIME_PAIRS_TO_TEST:,} pairs...")
    print(f"Maximum correction radius set to: {MAX_CORRECTION_RADIUS}")
    print("-" * 80)
    start_time = time.time()
    
    successful_corrections = []
    correction_failures = []
    law_ii_violations = []
    
    # CRITICAL: This set stores the unique composite k-values observed (Law II evidence)
    counterexample_ks = set() 
    
    radius_counts = {}

    # Start index must be high enough to accommodate the max radius check for S_{n-r}
    # Since n is the index of p_n, we start at MAX_CORRECTION_RADIUS + 1
    start_index = MAX_CORRECTION_RADIUS + 1 
    
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + start_index):
        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        if anchor_sum > SIEVE_LIMIT:
            print(f"WARNING: Anchor sum {anchor_sum:,} at index {i} has exceeded the SIEVE_LIMIT.")
            print("Stopping test to prevent inaccurate results.")
            break 

        # --- Law I Check ---
        min_distance_k = 0
        closest_primes_q = []
        d = 1
        
        while True:
            # Check both sides of the anchor for a prime
            found_lower = (anchor_sum - d) in prime_set
            found_upper = (anchor_sum + d) in prime_set
            
            if found_lower or found_upper:
                min_distance_k = d
                if found_lower:
                    closest_primes_q.append(anchor_sum - d)
                if found_upper:
                    closest_primes_q.append(anchor_sum + d)
                break 
            
            if (anchor_sum + d) > SIEVE_LIMIT: break
            d += 1
        
        if not closest_primes_q: continue

        # Check if this is a counterexample to Law I (composite k)
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            
            # --- Law II Check: Structured Exception ---
            # Composite k must be a product of ODD primes (i.e., must not have factor 2)
            if min_distance_k % 2 == 0:
                law_ii_violations.append({
                    "anchor": anchor_sum,
                    "k": min_distance_k,
                    "reason": "Composite k is EVEN (has factor 2)"
                })
                continue 
            
            # If Law II passes (k is odd composite), record it for the final report!
            counterexample_ks.add(min_distance_k)
            
            # --- Law III Check: Hierarchical Correction ---
            is_event_corrected = False
            
            for q_prime in closest_primes_q:
                is_this_q_corrected = False
                
                for radius in range(1, MAX_CORRECTION_RADIUS + 1):
                    correction_details = {}
                    
                    # 1. Test previous anchor: S_{n-radius}
                    idx_prev = i - radius
                    p_prev_1 = prime_list[idx_prev]
                    p_prev_2 = prime_list[idx_prev + 1]
                    s_prev = p_prev_1 + p_prev_2
                    k_prev = abs(s_prev - q_prime)

                    if k_prev == 1 or k_prev in prime_set:
                        is_this_q_corrected = True
                        correction_details = {"corrected_by": f"S_n-{radius}", "radius": radius, "new_k": k_prev}
                    
                    # 2. Test next anchor: S_{n+radius}
                    if not is_this_q_corrected:
                        idx_next = i + radius
                        p_next_1 = prime_list[idx_next]
                        p_next_2 = prime_list[idx_next + 1]
                        s_next = p_next_1 + p_next_2
                        k_next = abs(s_next - q_prime)

                        if k_next == 1 or k_next in prime_set:
                            is_this_q_corrected = True
                            correction_details = {"corrected_by": f"S_n+{radius}", "radius": radius, "new_k": k_next}

                    # If corrected, log the event and move to the next q_prime/event.
                    if is_this_q_corrected:
                        is_event_corrected = True
                        base_info = {"original_anchor": anchor_sum, "prime_q": q_prime, "composite_k": min_distance_k}
                        successful_corrections.append({**base_info, **correction_details})
                        radius_counts[radius] = radius_counts.get(radius, 0) + 1
                        break # Exit the radius loop for this q_prime.
                
                if is_event_corrected:
                    break # If any q_prime corrected, the event is resolved.
            
            # --- Law III Failure Log ---
            if not is_event_corrected:
                correction_failures.append({
                    "anchor": anchor_sum,
                    "failed_primes_q": closest_primes_q,
                    "k": min_distance_k,
                    "reason": f"Correction failed within r={MAX_CORRECTION_RADIUS}"
                })

        if (i + 1) % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"Processed {(i + 1) - start_index:,}/{MAX_PRIME_PAIRS_TO_TEST:,} pairs. Time elapsed: {elapsed:.2f}s.", end='\r')

    # --- FINAL REPORT GENERATION ---
    end_time = time.time()
    total_pairs_tested = (i + 1) - start_index
    total_exceptions = len(successful_corrections) + len(law_ii_violations) + len(correction_failures)

    print("\n\n" + "="*20 + " PRIME ANCHOR SYSTEM FINAL REPORT " + "="*20)
    print(f"Total Prime Pairs Processed: {total_pairs_tested:,}")
    print(f"Total Verification Time: {end_time - start_time:.2f} seconds")
    print("-" * 80)
    
    # Status Check
    if law_ii_violations or correction_failures:
        print("\n[ STATUS: CONJECTURE FAILED ] - ANOMALY DETECTED.")
    else:
        print("\n[ STATUS: CONJECTURE HOLDS ] - Verified successfully up to this limit.")

    # Law I & II Summary
    print(f"\nTotal Law I Failures (Composite k_min): {total_exceptions:,}")
    print(f"Law II Violations (Composite k was EVEN): {len(law_ii_violations):,}")
    
    if len(law_ii_violations) > 0:
        print("!!!!!!!!!!!!!!!!!!!! LAW II VIOLATION DETECTED !!!!!!!!!!!!!!!!!!!!")
        for violation in law_ii_violations[:5]:
            print(f"  Violation at Anchor {violation['anchor']}: k={violation['k']}")

    # --- Law II: Unique Composite k-Values Observed (The structure proof) ---
    print("\n" + "-"*15 + " Law II: Unique Composite k-Values Observed " + "-"*15)
    
    if counterexample_ks:
        # Sort the set for clean display
        sorted_k = sorted(list(counterexample_ks))
        print(f"Total unique composite k-values observed: {len(sorted_k)}")
        print("Set of observed k-values (must be products of odd primes):")
        print(sorted_k)
    else:
        print("No composite k-values were observed (implying k_min was always 1 or a prime).")
    
    # Law III Summary
    print(f"\nLaw III Correction Failures (Exceeded r={MAX_CORRECTION_RADIUS}): {len(correction_failures):,}")
    
    if len(correction_failures) > 0:
        print("!!!!!!!!!!!!!!!!!!! LAW III VIOLATION DETECTED !!!!!!!!!!!!!!!!!!!!")
        for failure in correction_failures[:5]:
            print(f"  Failure at Anchor {failure['anchor']}: k={failure['k']}")
            
    # Decay Analysis
    print("\n" + "-"*15 + " Law III: Deterministic Decay Analysis " + "-"*15)
    
    if len(successful_corrections) > 0:
        total_corrected = len(successful_corrections)
        sorted_radii = sorted(radius_counts.keys())
        cumulative_corrections = 0
        
        for r in sorted_radii:
            count = radius_counts[r]
            cumulative_corrections += count
            
            percent_of_exceptions = (count / total_corrected) * 100
            cumulative_percent = (cumulative_corrections / total_corrected) * 100
            
            print(f"Radius {r:2d}: {count:6,} corrections ({percent_of_exceptions:6.2f}%) | Cumulative: {cumulative_percent:6.2f}%")
        
        max_radius = sorted_radii[-1] if sorted_radii else 0
        print(f"\nMaximum Correction Radius Observed: {max_radius}")
    
    print("\n" + "="*80)

# --- Run the program ---
if __name__ == "__main__":
    test_correction_law()
