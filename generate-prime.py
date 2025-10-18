# ==============================================================================
# PRIME GENERATOR SCRIPT
# ==============================================================================
import math
import time

# --- Configuration for Prime Generation ---
TARGET_PRIMES = 100000000 + 1 + 101
PRIME_LIST_PATH = "primes_100m.txt"

def sieve_of_eratosthenes(limit):
    """Generates primes up to 'limit' using the Sieve of Eratosthenes."""
    limit = int(limit) 
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    return [p for p, is_p in enumerate(is_prime) if is_p]

def get_first_n_primes(n):
    """Estimates a limit and generates the first n primes."""
    # A safe overestimation for the Sieve to capture the Nth prime
    limit_estimate = int(n * (math.log(n) + math.log(math.log(n))))
    
    print(f"Generating primes up to approximately {limit_estimate:,} (Target: {n:,} primes)...")
    start_time = time.time()
    primes = sieve_of_eratosthenes(limit_estimate)
    end_time = time.time()
    print(f"Sieve completed in {end_time - start_time:.2f} seconds.")

    return primes[:n]

def run_generator():
    prime_list = get_first_n_primes(TARGET_PRIMES)
    
    if len(prime_list) != TARGET_PRIMES:
        print(f"WARNING: Could only find {len(prime_list)} primes. Target was {TARGET_PRIMES}.")

    # Save to file
    with open(PRIME_LIST_PATH, 'w') as f:
        for p in prime_list:
            f.write(str(p) + '\n')
            
    print("-" * 50)
    print(f"SUCCESS: Saved {len(prime_list):,} primes to {PRIME_LIST_PATH}")
    print(f"You can now run the analysis script.")
    print("-" * 50)

if __name__ == "__main__":
    run_generator()
