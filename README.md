# The Prime Anchor System (Version 7.0 - The Modulo 6 Resolution)

**Date:** October 17, 2025

**Author:** Independent Researcher (City of Malabon, Metro Manila, Philippines)

**Verification Extent:** First 4,000,000 consecutive prime pairs (p_n, p_{n+1})

---

## Abstract

This paper presents the complete findings of a computational investigation into the **Prime Anchor System**. The project began with the discovery of a significant, non-random bias in the local distribution of primes. An initial null hypothesis test confirmed this bias to be a real **+2.55%** structural advantage over a random baseline. However, thanks to a critical insight from the mathematical community, a definitive follow-up test was conducted. This final test proved that the entire observed bias is elegantly and completely explained by a known arithmetic property: the sum of two consecutive primes is almost always a multiple of 6.

While this solves the initial mystery of the bias, it does not explain the system's robust, hierarchical correction mechanism (Law III). The focus of the conjecture now shifts to the remaining analytical challenge: to explain the hyper-local and structurally constrained nature of this corrective law.

---

## 1. Core Definitions

The system is built upon two fundamental definitions:

1.  **The Anchor Point (S_n):** The sum of any two consecutive prime numbers, $S_n = p_n + p_{n+1}$.
2.  **The Distance (k):** The absolute difference between an Anchor Point ($S_n$) and any given prime number q, $k = |S_n - q|$.

---

## 2. The Hierarchical Laws of the System

### Law I: The Primary Observed Phenomenon

This law describes the pattern that initiated the investigation.

**Observation:** For any Anchor Point ($S_n$), the distance $k_{min}$ to the nearest prime shows a strong tendency to be a "clean" value ($k_{min} \in \{1, \mathbb{P}\}$).

### Law II: The Law of Structured Exception

This law governs the nature of the rare failures of Law I, revealing that the exceptions are not random.

**Observation:** In the rare instances where Law I fails and $k_{min}$ is a composite number, this composite is always a product of prime numbers (e.g., `{9, 15, 21, 25, ...}`).

### Law III: The Law of Hierarchical Correction (The Unexplained Mechanism)

This is the most novel part of the system. It demonstrates a universal, self-correcting property that is **not** explained by the modulo 6 property.

**Conjecture:** Any prime that fails the primary alignment from $S_n$ is **always resolved** to a clean distance by measuring it from a nearby anchor, $S_{n \pm r}$. Computational tests over 4M pairs show this correction is hyper-local, with a maximum observed radius of **$r_{max}=14$**.

---

## 3. The Definitive Computational Finding: Solving the Bias Mystery

The entire investigation culminated in a final, definitive experiment to determine the cause of the observed bias. A test was run comparing three groups over 3,999,999 pairs.

| Group | Success Rate | Description |
| :--- | :--- | :--- |
| **P_Observed** (Prime Anchors) | **46.68%** | The original experimental group. |
| **P'_Baseline** (Random Evens) | **44.13%** | The initial control group. |
| **P''_Mod6_Baseline** (Random Mult of 6) | **51.46%** | The definitive, hyper-fair control group. |

**Conclusion:** The results are unambiguous. The "modulo 6" property provides a massive structural advantage. The fact that the Prime Anchors (46.68%) perform significantly worse than random multiples of 6 (51.46%) proves that the "modulo 6" property is the complete and sole explanation for the originally observed bias.

---

## 4. The New Analytical Challenge: The `r_max` Mystery

With the mystery of the bias now solved, the central analytical challenge shifts entirely to the unexplained nature of Law III. The "modulo 6" property explains the successes, but it tells us nothing about the system's elegant and efficient handling of its failures.

The new question is therefore:

**Why is the hierarchical correction for the failures of this "modulo 6" alignment so structurally constrained and hyper-local? What is the true growth function of `r_max(p_n)`?**
