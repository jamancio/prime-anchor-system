# ==============================================================================
# The Prime Anchor System Tester (Version 10.0 - Final)
#
# This script is the definitive tool for testing the complete, three-part
# "Prime Anchor System" conjecture.
#
# 1. It finds all counterexamples to the main conjecture (Law I).
# 2. It verifies that the "Law of Correction" (Law III) holds true for
#    every one of these counterexamples.
#
# A "Correction Failure" would disprove the entire unified theory.
#
# Origin: Formulated on October 16, 2025, in the Philippines.
# ==============================================================================

import math
import time

# --- Configuration ---
# To test more pairs, increase both of these numbers.
# SIEVE_LIMIT should be at least 20-30x larger than MAX_PRIME_PAIRS_TO_TEST.
SIEVE_LIMIT = 3000000 # Increased for a more robust default test
MAX_PRIME_PAIRS_TO_TEST = 100000

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
    """Tests the Law of Correction on all counterexamples to the main conjecture."""
    prime_list, prime_set = sieve_for_primes(SIEVE_LIMIT)

    if len(prime_list) < MAX_PRIME_PAIRS_TO_TEST + 3: # Need i+2 for S_n+1
        print(f"Error: Sieve limit is too low. Please increase SIEVE_LIMIT.")
        return

    print(f"\nStarting test of the Law of Correction for the first {MAX_PRIME_PAIRS_TO_TEST} pairs...")
    print("This will only report on counterexamples to the main conjecture.")
    print("-" * 80)
    start_time = time.time()
    
    successful_corrections = []
    correction_failures = []
    counterexample_ks = set()

    # We start at index 2 (pair p3,p4) to ensure we always have a p_{n-1} available (p2)
    for i in range(2, MAX_PRIME_PAIRS_TO_TEST + 1):
        p_n = prime_list[i]
        p_n_plus_1 = prime_list[i+1]
        anchor_sum = p_n + p_n_plus_1

        # Find the absolute closest prime to this anchor
        min_distance_k = 0
        closest_prime_q = 0
        d = 1
        while True:
            # Check both sides. The first one we hit is the closest.
            if (anchor_sum - d) in prime_set:
                closest_prime_q = anchor_sum - d
                min_distance_k = d
                break
            if (anchor_sum + d) in prime_set:
                closest_prime_q = anchor_sum + d
                min_distance_k = d
                break
            if (anchor_sum + d) > SIEVE_LIMIT: return # Safety break
            d += 1

        # Now, check if this is a counterexample to the main conjecture (Law I)
        is_k_composite = (min_distance_k > 3) and (min_distance_k not in prime_set)
        
        if is_k_composite:
            # We found a counterexample! Now test the Law of Correction (Law III).
            counterexample_ks.add(min_distance_k)
            is_corrected = False
            correction_details = {}

            # Test previous anchor: S_{n-1}
            p_n_minus_1 = prime_list[i-1]
            s_prev = p_n_minus_1 + p_n
            k_prev = abs(s_prev - closest_prime_q)
            if k_prev == 1 or k_prev in prime_set:
                is_corrected = True
                correction_details = {"corrected_by": "S_n-1", "new_k": k_prev, "new_anchor": s_prev}

            # Test next anchor: S_{n+1} (only if not already corrected)
            if not is_corrected:
                p_n_plus_2 = prime_list[i+2]
                s_next = p_n_plus_1 + p_n_plus_2
                k_next = abs(s_next - closest_prime_q)
                if k_next == 1 or k_next in prime_set:
                    is_corrected = True
                    correction_details = {"corrected_by": "S_n+1", "new_k": k_next, "new_anchor": s_next}

            base_info = { "original_anchor": anchor_sum, "prime_q": closest_prime_q, "composite_k": min_distance_k }
            if is_corrected:
                successful_corrections.append({**base_info, **correction_details})
            else:
                correction_failures.append(base_info)

    end_time = time.time()
    print(f"Analysis completed in {end_time - start_time:.2f} seconds.")
    print("-" * 80)

    # --- Final Reports ---
    print("\n" + "="*20 + " FINAL ANALYSIS REPORT " + "="*20)

    if not correction_failures:
        print("\n[ STATUS: LAW OF CORRECTION VERIFIED ]")
        print("The Law of Correction holds true for all counterexamples found.")
        print(f"A total of {len(successful_corrections)} corrections were successfully verified.")
    else:
        print("\n[ STATUS: LAW OF CORRECTION DISPROVEN ]")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("FAILURE! The Law of Correction has been DISPROVEN.")
        print(f"Found {len(correction_failures)} instance(s) where the correction failed:")
        for failure in correction_failures:
            print(failure)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print("\n" + "-"*20 + " Law of Structured Exception Report " + "-"*20)
    print("The unique composite k-values found in the exceptions were:")
    print(sorted(list(counterexample_ks)))

    print("\n" + "-"*20 + " Verified Corrections Log (First 50) " + "-"*20)
    print(f"{'Original Anchor':<15} | {'Prime':<10} | {'Bad k':<7} | {'Corrected By':<12} | {'New Anchor':<12} | {'Good k':<7}")
    print("-" * 75)
    for s in successful_corrections[:50]:
        print(f"{s['original_anchor']:<15} | {s['prime_q']:<10} | {s['composite_k']:<7} | {s['corrected_by']:<12} | {s['new_anchor']:<12} | {s['new_k']:<7}")
    print("-" * 75)

# --- Run the program ---
if __name__ == "__main__":
    test_correction_law()

