# ==============================================================================
# STEP 1: PRIME GENERATOR (The Slow, Pre-computation Step)
# This script computes the first 2,000,001 primes and saves them to a file.
# This prevents timeout errors during the main analysis loop.
# ==============================================================================

import math
import time

# --- Configuration ---
NUM_PRIMES_TO_GENERATE = 2000001
OUTPUT_FILENAME = "primes_2m.txt"

def sieve_of_eratosthenes(limit):
    """Generates primes up to 'limit' using the Sieve of Eratosthenes."""
    limit = int(limit)
    if limit < 2:
        return []

    print(f"Starting Sieve up to {limit:,}...")
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False

    return [p for p, is_p in enumerate(is_prime) if is_p]

def generate_and_save_primes(n):
    """Estimates limit, generates primes, and saves the list."""
    start_time = time.time()
    
    # Estimate the upper limit required using the Prime Number Theorem approximation
    if n < 6: return
    limit_estimate = int(n * (math.log(n) + math.log(math.log(n))))

    print(f"Estimated limit needed: {limit_estimate:,}")
    primes = sieve_of_eratosthenes(limit_estimate)
    
    # Ensure we have the required number of primes
    if len(primes) < n:
        print(f"Error: Sieve limit was slightly too low. Found {len(primes):,}, needed {n:,}. Try increasing the SIEVE_LIMIT in the script.")
        return

    # Slice to the exact count needed and save
    final_primes = primes[:n]
    
    with open(OUTPUT_FILENAME, 'w') as f:
        # Write each prime on a new line for easy loading
        for p in final_primes:
            f.write(f"{p}\n")
    
    end_time = time.time()
    print("-" * 50)
    print(f"SUCCESS: Saved {len(final_primes):,} primes to {OUTPUT_FILENAME}")
    print(f"Total generation time: {end_time - start_time:.2f} seconds.")
    print("-" * 50)

if __name__ == "__main__":
    generate_and_save_primes(NUM_PRIMES_TO_GENERATE)
