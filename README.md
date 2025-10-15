# The Prime Anchor System

A multi-layered conjecture on the local distribution of prime numbers.

## Overview

This repository contains the research and testing code for the Prime Anchor System, a hierarchical set of conjectures that proposes a deep, non-random, and self-correcting structure governing the local distribution of prime numbers.

This system suggests that the primes are not random islands, but are connected by an elegant and predictable set of interlocking rules.

### The Theory: The Three Laws of the System

The system is defined by a primary law, a law for its exceptions, and a law for correcting those exceptions.

Core Definition: The Anchor Point (S_n)

The "Anchor Point" is the sum of any two consecutive prime numbers (p_n, p_{n+1}).

## Law I: The Prime Anchor Conjecture (The Main Rule)

**Conjecture**: For any Anchor Point (S_n), the prime number q that is absolutely closest to it will almost always be found at a distance k that is either 1 or a prime number.

This law is overwhelmingly strong, but our testing has shown that it is not absolute. This led to the discovery of the second law.

## Law II: The Law of Structured Exception

This law governs the rare cases where Law I fails. The exceptions are not random.

**Conjecture**: When the closest prime to an anchor is at a composite distance k, this composite k will always be a product of small, odd prime numbers.

Evidence (from the first 100,000 prime pairs):
The set of unique composite k values found in the counterexamples to Law I is: [9, 15, 21, 25, 27, 33, 35, 39, 45, 49, 51, 55, 57, 65]. The prime factors of every number on this list are from the set {3, 5, 7, 11, 13, 17, 19}.

## Law III: The Law of Correction
This is the most critical part of the system, as it makes the entire theory self-consistent.

**Conjecture**: Any prime q that is found at a "messy" composite distance k from one anchor (S_n) can be "corrected." It can always be found from an adjacent anchor point (S_{n-1} or S_{n+1}) with a new, "clean" distance k_new that is 1 or a prime number.

# The Code: prime_anchor_system_tester.py

This repository contains the Python script used to test and verify the entire system.

### Purpose:
The script is designed to hunt for counterexamples to Law I and, upon finding one, immediately test if the Law of Correction holds true. A failure of Law III would disprove the entire theory.
How to Run:
1. Ensure you have Python 3 installed.
2. Run the script from your terminal: python prime_anchor_system_tester.py
3. The script will first generate a large list of primes (the "sieve") and then begin testing.

### How to Configure:
You can easily change the scale of the test by modifying the two variables at the top of the script:
- MAX_PRIME_PAIRS_TO_TEST: The number of prime pairs to analyze.
- SIEVE_LIMIT: The upper bound for prime number generation. This must be significantly larger than the expected anchor sums.
Current Findings (as of October 16, 2025)
- Law I has been shown to have exceptions (e.g., the anchor 263+269=532, where the closest prime is at k=9).
- Law II has been verified against all exceptions found in the first 100,000 prime pairs. The composite k values consistently show a pattern of small, odd prime factors.
- Law III has been successfully verified for all exceptions found in the first 100,000 prime pairs. To date, no counterexample to the Law of Correction has been found.

### How to Contribute
This is an ongoing exploration, and community help is invaluable.
1. Hunt for the Ultimate Counterexample: The biggest contribution would be to find a failure of the Law of Correction. This would be a case where a prime q is at a composite distance k from an anchor S_n, and neither of the adjacent anchors (S_{n-1} or S_{n+1}) can connect to it with a prime or 1 distance.
2. Optimize the Code: The current script is written for clarity, not for maximum speed. If you have expertise in high-performance computing, your optimizations would be welcome.
3. Mathematical Analysis: If you have a background in number theory, any insights into the underlying mathematical reasons for these laws would be a major contribution.

This system was formulated during a collaborative session on Thursday, October 16, 2025.
