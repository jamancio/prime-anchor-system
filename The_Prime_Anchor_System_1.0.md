# The Prime Anchor System

A multi-layered conjecture on the local distribution of prime numbers.

## Overview

Hello, and welcome. This repository documents a conjecture I call the Prime Anchor System. I'm not a formal mathematician, but an enthusiast who has long been fascinated by prime numbers. This is a system of rules I've developed that appears to describe a hidden, deterministic structure in their distribution.

The purpose of this repository is to share my findings and invite scrutiny, testing, and collaboration from the community. I believe the best way to know if an idea has merit is to ask for help trying to break it.

The purpose of making this research public is to invite scrutiny, testing, and falsification from the mathematics and computer science communities.

This system suggests that the primes are not random islands, but are connected by an elegant and predictable set of interlocking rules.

### The Theory: The Three Laws of the System

The system suggests that primes are not random, but are connected by an elegant set of interlocking rules centered on "Anchor Points."

### Core Definition: The Anchor Point (S_n)

An "Anchor Point" is simply the sum of any two consecutive prime numbers (e.g., p_n + p_{n+1}). These points act as centers of influence for all other primes.

## Law I: The Prime Anchor Conjecture (The Main Rule)

This is the dominant pattern that holds true in the vast majority of cases.

**Conjecture**: For any Anchor Point (S_n), the prime number q that is absolutely closest to it will almost always be found at a distance k that is either 1 or a prime number.

This law is overwhelmingly strong, but our testing has shown that it is not absolute. This led to the discovery of the second law.

## Law II: The Law of Structured Exception

This law governs the rare cases where Law I fails, revealing that the exceptions are not random.

**Conjecture**: When the closest prime to an anchor is at a composite distance k, this composite k will always be a product of small, odd prime numbers (e.g., 9, 15, 21, 25...).

Evidence (from the first 100,000 prime pairs):
The set of unique composite k values found in the counterexamples to Law I is: [9, 15, 21, 25, 27, 33, 35, 39, 45, 49, 51, 55, 57, 65]. The prime factors of every number on this list are from the set {3, 5, 7, 11, 13, 17, 19}.

## Law III: The Law of Hierarchical Correction

This is the most critical part of the system, making it self-consistent. Its current form was discovered by analyzing a failure in an earlier, simpler version.

My initial thought was that a "messy" prime could always be "corrected" by looking at the immediately adjacent anchors (S_{n-1} or S_{n+1}). However, the testing code I wrote disproved this. By carefully analyzing the first failure, a deeper, hierarchical rule was revealed:

**Conjecture**: Any prime q found at a "messy" composite distance from an anchor can always be resolved to a "clean" distance (1 or a prime) by expanding a search to nearby anchors. The system does this algorithmically:

1. Radius 1: It first checks the immediately adjacent anchors (S_{n-1}, S_{n+1}). This resolves most cases.
2. Radius 2+: If, and only if, a correction is not found, the protocol expands the search to the next set of anchors (S_{n-2}, S_{n+2}), and continues outwards until a resolution is found.

# The Code: prime_anchor_system_tester.py

This repository contains the Python script used to test and verify the entire system. It is designed to hunt for exceptions to Law I and then immediately test if the hierarchical Law of Correction holds true.

### Purpose:
The script is designed to hunt for counterexamples to Law I and, upon finding one, immediately test if the Law of Correction holds true. A failure of Law III would disprove the entire theory.
How to Run:
1. Ensure you have Python 3 installed.
2. Run the script from your terminal: python prime_anchor_system_tester.py
3. The script will first generate a large list of primes (the "sieve") and then begin testing.

### Current Findings 

**(as of October 16, 2025)**:
The hierarchical Law of Correction has been successfully verified for all exceptions found. To date, no counterexample has been found that defies this expanded search protocol.

Tested up to **500,000** pairs and the theory still stands.

### How to Contribute
This is an ongoing exploration, and any help is invaluable.

1. Hunt for the Ultimate Counterexample: The most significant contribution would be to find a failure of the hierarchical Law of Correction. This would require finding a "messy" prime that cannot be corrected even after expanding the search radius.
2. Optimize the Code: The script is written for clarity, not maximum speed. If you have expertise in high-performance computing, your optimizations would be very welcome.
3. Mathematical Analysis: If you have a background in number theory, any insights into the underlying mathematical reasons why these laws might be true would be a major contribution.

This system was formulated during a collaborative session on Thursday, October 16, 2025.
