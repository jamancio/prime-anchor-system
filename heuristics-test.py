import math
import time

def sieve_of_eratosthenes(limit):
    """Generates primes up to 'limit' using the Sieve of Eratosthenes."""
    # Ensure limit is an integer before proceeding
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
    if n < 6:
        return [2, 3, 5, 7, 11, 13][:n]

    # Calculate the limit estimate and explicitly cast to int
    limit_estimate = int(n * (math.log(n) + math.log(math.log(n))))
    
    print(f"Generating primes up to approximately {limit_estimate:,}...")
    primes = sieve_of_eratosthenes(limit_estimate)
    
    return primes[:n]

def run_heuristic_analysis(num_primes):
    """
    Performs the two-part analysis:
    1. Calculates the Empirical Frequency (P_Observed).
    2. Calculates the Expected Random Baseline (P_Expected).
    """
    print(f"--- Running Heuristic Analysis for the first {num_primes:,} primes... ---")
    
    start_time_prime_gen = time.time()
    all_primes = get_first_n_primes(num_primes + 1)
    end_time_prime_gen = time.time()
    
    if len(all_primes) < num_primes + 1:
        print("Error: Could not generate enough primes.")
        return

    prime_set = set(all_primes)
    
    total_anchors = num_primes - 1  
    clean_k_count = 0
    max_k_min = 0 # max_k_min initialized as an integer
    
    start_time_analysis = time.time()

    # --- Part 1: Empirical Test (P_Observed and R_max) ---
    for i in range(1, num_primes):
        p_n = all_primes[i]
        p_n_plus_1 = all_primes[i+1]
        s_n = p_n + p_n_plus_1  

        k_min = 0 # k_min will now be assigned an integer value in the search
        
        # Search outward from S_n for the closest prime q
        search_radius = 1
        
        while search_radius <= 500: 
            q_lower = s_n - search_radius
            q_upper = s_n + search_radius
            
            found_q = False
            
            # Check lower bound
            if q_lower > 1 and q_lower in prime_set:
                k_min = search_radius
                found_q = True
            
            # Check upper bound
            if q_upper in prime_set:
                k_min = search_radius
                found_q = True

            if found_q:
                break
                
            search_radius += 1

        # Tally the result for Law I (k_min is 'clean' if 1 or prime)
        is_clean = (k_min == 1) or (k_min > 1 and k_min in prime_set)
        if is_clean:
            clean_k_count += 1
        
        # Update the maximum k_min observed for the R_max baseline
        if k_min > max_k_min:
            max_k_min = k_min

    end_time_analysis = time.time()

    # --- Part 2: Expected Random Baseline (P_Expected) ---
    
    # R_max is now explicitly guaranteed to be an integer (int(max_k_min))
    R_max = int(max_k_min) 
    
    # 1. Count all possible k values (all odd integers in the range [1, R_max])
    total_possible_k = (R_max + 1) // 2 
    
    # 2. Count all "clean" k values (1 + all primes in the range [3, R_max])
    primes_up_to_R = sieve_of_eratosthenes(R_max)
    
    # Count of primes (excluding 2)
    primes_count = len(primes_up_to_R) - 1 
    
    # Total clean k values: 1 (for k=1) + primes_count
    total_clean_k = primes_count + 1 
    
    # Calculate the Expected Random Probability (P_Expected)
    p_expected = total_clean_k / total_possible_k

    # --- Final Output ---
    
    p_observed = clean_k_count / total_anchors
    
    print(f"\n--- Results Summary (Tested over {total_anchors:,} Anchor Points) ---")
    print(f"Prime Generation Time: {end_time_prime_gen - start_time_prime_gen:.2f} seconds")
    print(f"Analysis Time: {end_time_analysis - start_time_analysis:.2f} seconds")
    print("-" * 60)
    print(f"Maximum Observed Closest Distance (R_max): {R_max:,}")
    print(f"Total possible ODD distances in range [1, {R_max}]: {total_possible_k:,}")
    print(f"Total 'Clean' (1 or Prime) ODD distances in range: {total_clean_k:,}")
    print("-" * 60)
    print(f"P_Expected (Random Baseline): {p_expected:.4f} ({p_expected * 100:.2f}%)")
    print(f"P_Observed (Empirical Result): {p_observed:.4f} ({p_observed * 100:.2f}%)")
    
    difference = p_observed - p_expected
    print("-" * 60)
    if difference > 0.05:
        print(f"SUCCESS: Heuristic Justification: Observed frequency is {difference * 100:.2f} percentage points HIGHER than the random baseline. This formally suggests a **non-random, deterministic bias** in the prime distribution around the Anchor Points.")
    elif difference > 0:
        print(f"WARN: Initial Indication: Observed frequency is slightly higher, but the difference ({difference * 100:.2f}%) requires more rigorous statistical testing.")
    else:
        print("FAILED: Heuristic Justification Failed: Observed frequency is not above the random baseline.")
    
    print("-" * 60)


# Execute the analysis on the requested scale.
RUN_COUNT = 200_000
run_heuristic_analysis(num_primes=RUN_COUNT)
