# ==============================================================================
# The Prime Anchor System Tester (Version 12.0 - Hierarchical)
#
# This script is the definitive tool for testing the complete, three-part
# "Prime Anchor System" conjecture. It has been updated to include the
# "Law of Hierarchical Correction," which was discovered after an earlier,
# simpler version of the theory was disproven by a previous version of this code.
#
# The script's logic follows the full, updated theory:
# 1. It finds all counterexamples to Law I (a prime at a composite distance).
# 2. For each exception, it tests the hierarchical Law of Correction (Law III)
#    by searching for a "clean" prime distance at an expanding radius.
#
# A failure is only logged if a correction cannot be found within the
# maximum defined search radius.
#
# Origin: Formulated on October 16, 2025, in the City of Malabon, Philippines.
# ==============================================================================

import math
import time

# --- Configuration ---
# To test more pairs, you can increase these numbers.
# SIEVE_LIMIT should be large enough to contain all potential primes and anchors.
SIEVE_LIMIT = 3000000
MAX_PRIME_PAIRS_TO_TEST = 100000
MAX_CORRECTION_RADIUS = 5 # The maximum distance to search for a correcting anchor.

# --- Sieve of Eratosthenes for Prime Generation ---
def sieve_for_primes(limit):
    """Generates a list of primes and a set for fast primality testing."""
    print(f"Generating primes up to {limit}...")
    start_time = time.time()
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p*p, limit + 1, p):
                is_prime[multiple] = False

    prime_set = set()
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
            prime_set.add(p)
            
    end_time = time.time()
    print(f"Generated {len(primes)} primes in {end_time - start_time:.2f} seconds.")
    return primes, prime_set

# --- Main Testing Logic ---

def test_correction_law():
    """Tests the hierarchical Law of Correction."""
    prime_list, prime_set = sieve_for_primes(SIEVE_LIMIT)

    # Ensure we have enough primes for the largest possible radius check
    if len(prime_list) < MAX_PRIME_PAIRS_TO_TEST + MAX_CORRECTION_RADIUS + 3:
        print(f"Error: Sieve limit is too low for the given MAX_CORRECTION_RADIUS.")
        return

    print(f"\nStarting hierarchical test for the first {MAX_PRIME_PAIRS_TO_TEST} pairs...")
    print(f"Maximum correction radius set to: {MAX_CORRECTION_RADIUS}")
    print("-" * 80)
    start_time = time.time()
    
    successful_corrections = []
    correction_failures = []
    counterexample_ks = set()

    # Start index must be high enough to accommodate the max radius check for S_{n-r}
    start_index = MAX_CORRECTION_RADIUS + 1
    for i in range(start_index, MAX_PRIME_PAIRS_TO_TEST + 1):
        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        if anchor_sum >= SIEVE_LIMIT:
            print(f"WARNING: Anchor sum {anchor_sum} at index {i} has exceeded the SIEVE_LIMIT.")
            print("Stopping test to prevent inaccurate results.")
            break # Stop the main loop

        # Find all absolute closest primes to this anchor.
        # This was a key bug fix: we must account for equidistant primes (e.g., S_n +/- k).
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
                break # Found the minimum distance, so we can stop searching.
            
            if (anchor_sum + d) > SIEVE_LIMIT: break
            d += 1
        
        if not closest_primes_q: continue

        # Now, check if this is a counterexample to Law I.
        is_k_composite = (min_distance_k > 1) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            counterexample_ks.add(min_distance_k)
            # A Law I Failure was found. Begin hierarchical correction test for each prime found.
            is_event_corrected = False
            
            for q_prime in closest_primes_q:
                is_this_q_corrected = False
                
                # --- HIERARCHICAL CORRECTION LOOP ---
                # This is the core of the updated Law III. We expand the search radius
                # until a correction is found or we hit the max limit.
                for radius in range(1, MAX_CORRECTION_RADIUS + 1):
                    correction_details = {}
                    
                    # Test previous anchor at the current radius: S_{n-radius}
                    p_prev_1 = prime_list[i - radius]
                    p_prev_2 = prime_list[i - radius + 1]
                    s_prev = p_prev_1 + p_prev_2
                    k_prev = abs(s_prev - q_prime)

                    if k_prev == 1 or k_prev in prime_set:
                        is_this_q_corrected = True
                        correction_details = {"corrected_by": f"S_n-{radius}", "radius": radius, "new_k": k_prev, "new_anchor": s_prev}
                    
                    # Test next anchor if not already corrected by the previous one
                    if not is_this_q_corrected:
                        p_next_1 = prime_list[i + radius]
                        p_next_2 = prime_list[i + radius + 1]
                        s_next = p_next_1 + p_next_2
                        k_next = abs(s_next - q_prime)

                        if k_next == 1 or k_next in prime_set:
                            is_this_q_corrected = True
                            correction_details = {"corrected_by": f"S_n+{radius}", "radius": radius, "new_k": k_next, "new_anchor": s_next}

                    # If we found a correction for this q_prime, log it and stop searching for it.
                    if is_this_q_corrected:
                        is_event_corrected = True
                        base_info = {"original_anchor": anchor_sum, "prime_q": q_prime, "composite_k": min_distance_k}
                        successful_corrections.append({**base_info, **correction_details})
                        break # Exit the radius loop for this q_prime.
                # --- END HIERARCHICAL LOOP ---

                # If this q_prime was corrected, the whole event is considered resolved.
                # We can stop checking other equidistant primes for this event.
                if is_event_corrected:
                    break
            
            # A failure is only logged if ALL primes at the composite distance failed correction.
            if not is_event_corrected:
                correction_failures.append({
                    "original_anchor": anchor_sum,
                    "failed_primes_q": closest_primes_q,
                    "composite_k": min_distance_k
                })

    end_time = time.time()
    print(f"Analysis completed in {end_time - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " FINAL ANALYSIS REPORT " + "="*20)
    if not correction_failures:
        print("\n[ STATUS: HIERARCHICAL LAW OF CORRECTION VERIFIED ]")
        print(f"The system holds true. All {len(successful_corrections)} exceptions were successfully corrected.")
    else:
        print("\n[ STATUS: ANOMALY DETECTED ]")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("FAILURE! An uncorrected anomaly has been found.")
        print(f"Found {len(correction_failures)} instance(s) where correction failed within radius {MAX_CORRECTION_RADIUS}:")
        for failure in correction_failures:
            print(failure)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print("\n" + "-"*20 + " Law II Report: Composite k-Values Found " + "-"*20)
    print("The unique composite k-values found in the exceptions were:")
    print(sorted(list(counterexample_ks)))

    print("\n" + "-"*20 + " Verified Corrections Log (First 50) " + "-"*20)
    print(f"{'Original Anchor':<15} | {'Prime':<10} | {'Bad k':<7} | {'Corrected By':<12} | {'Radius':<7} | {'New k':<7}")
    print("-" * 75)
    for s in successful_corrections[:50]:
        print(f"{s['original_anchor']:<15} | {s['prime_q']:<10} | {s['composite_k']:<7} | {s['corrected_by']:<12} | {s['radius']:<7} | {s['new_k']:<7}")
    print("-" * 75)

# --- Run the program ---
if __name__ == "__main__":
    test_correction_law()

