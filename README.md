# The Prime Anchor System: A Conclusive Report (Version 9.1)

**Date:** October 19, 2025

**Author:** Independent Researcher (City of Malabon, Metro Manila, Philippines)

**Verification Extent:** First 50,000,000 consecutive prime pairs ($P_n$, $P_{n+1}$)

---

## Abstract: The Solved Puzzle

This document presents the final and complete findings of the **Prime Anchor System** investigation. The research began as a conjecture on a non-random "bias" in prime distribution (v1.0-v5.0). This bias was proven to be a deterministic **"Modulo 6 Filter"** (v6.0-v7.0), which fully explained the behavior of Laws I and II.

The investigation then pivoted to the system's "r_max Mystery" (v8.0): the 100% self-correcting nature of Law III. A series of definitive "showdown" tests over 50,000,000 pairs proved that this 100% correction rate is a general property of the **"Prime Neighborhood Saturation"**, a "dense neighborhood" of fixes where *any* sufficiently filtered search protocol (even random ones) will find a 100% correction rate.

The final test (Test 10) definitively compared the efficiency of the original $S_n$ system against a "Perfected $\pmod{210}$" system. The results proved the $\pmod{210}$ system is **conclusively superior**, with a 94.32% "instant fix" rate and a smaller $r_{max}=10$, compared to the $S_n$ system's 75.85% instant fix rate and $r_{max}=16$. This demonstrates that the efficiency observed is a function of the **"Primorial Filter"** strength, not a unique property of the $S_n$ sequence. The original $S_n$ system is thus rendered obsolete, having served as the crucial prototype that led to the discovery of the true, efficient filtering mechanism.

---

## 1. The Initial Conjecture (The Journey)

The investigation began with a simple set of definitions and a three-part conjecture:

* **The Anchor Point ($S_n$):** The sum of two consecutive primes, $S_n = P_n + P_{n+1}$.
* **The Distance ($k$):** The distance from an anchor to any prime $q$, $k = |S_n - q|$.

The system was originally defined by three hierarchical laws:
* **Law I (Original Name: "Rule of Proximity"):** The initial observation was that the nearest prime $q$ to a specific anchor $S_n$ would almost always be at a "clean" distance ($k=1$ or $k=\mathbb{P}$). As the research evolved, this was understood to be a manifestation of a more general phenomenon, now termed **Law of Local Prime Alignment**. This law describes the observable tendency for primes to align at clean distances around anchor points.
* **Law II (Exception):** The rare composite $k$ failures were structured (e.g., 9, 15, 21...). This describes the nature of the failures when the Local Prime Alignment does not hold for the nearest prime.
* **Law III (Correction):** The initial hypothesis was that any "messy" failure from $S_n$ would be "fixed" by a nearby anchor $S_{n \pm r}$. This hypothesis about the specific corrective role of the $S_n$ sequence was later disproven. **However, the initial step of identifying a 'Law I failure' (a composite $k_{min}$) remains defined relative to the original $S_n = P_n + P_{n+1}$ anchor, which serves as the detector for these 'messy prime events' before a more efficient corrective search (like the $\pmod{210}$ system) is applied.**

---

## 2. The Solved Mystery of Laws I & II (The "Modulo 6 Filter")

The first great discovery of this research was the complete resolution of Laws I and II.

* **The "Bias":** Initial testing showed a persistent statistical bias. For example, v6.0 showed a **+2.55%** advantage for $S_n$ anchors over a simple random baseline.
* **The "Modulo 6" Insight:** A follow-up test (v7.0) against a "hyper-fair" baseline of random multiples of 6 *reversed* this bias.
* **The Final Proof (Test 2):** A definitive "classifier" test proved that Laws I and II are not a "bias" but a **deterministic "Modulo 6 Filter."** It was proven that the $S_n \pmod 6$ value of an anchor (0, 2, or 4) *perfectly predicts* the *type* of failure it is vulnerable to.

This discovery fully solved the initial mystery of the system's "bias."

---

## 3. The Final Definitive Test (The "Primorial Filter" Hierarchy)

With Laws I & II solved, the investigation shifted to the $r_{max}$ mystery. Was the $S_n$ system's 100% correction rate special, or just an artifact?

A series of "showdown" tests over 50,000,000 pairs was conducted to compare the efficiency of different corrective systems. The final, definitive test [Test 10](r-max-efficiency.py) compared the *full deterministic decay curve* of the $S_n$ system against a "Perfected $\pmod{210}$" system, while also tracking the success rates and maximum search depths of various random control systems.

The results confirmed that **all tested systems achieved a 100% correction rate**, highlighting the "Dense Neighborhood" saturation. However, they also revealed a clear hierarchy of efficiency, demonstrating the power of the "Primorial Filter" ($P_{k_{th}} = 2 \times 3 \times \dots \times p_k$):

| System | Anchor Type | $r=1$ Fix Rate | Max Search Depth ($r_{max}$) |
| :--- | :--- | :--- | :--- |
| **System D (Even Random)** | Random $\pmod 2$ | N/A (Low) | $e_{max} \approx 40$ (Least Efficient) |
| **System C (Mod 6 Random)** | Random $\pmod 6$ ($P_{2_th}$) | ~84% | $c_{max} \approx 20$ |
| **System A ($S_n$ System)** | Deterministic $S_n$ ($\approx \pmod{30}$) | 75.85% | $r_{max} = 16$ |
| **System B ($\pmod{30}$ Random)**| Random $\pmod{30}$ ($P_{3_th}$) | ~90% | $c_{max} \approx 13-19$ |
| **System E ($\pmod{210}$ System)**| **Perfected $\pmod{210}$ ($P_{4_th}$)** | **94.32%** | **$r_{max} = 10$ (Most Efficient)** |

*(Note: Random system r=1 rates are approximate based on a previous [tests](r-max-analysis.py))*

---

## 4. Final Conclusion (The Solved Puzzle)

The "Deterministic Decay Showdown" (Test 10) provides the conclusive answer to the Prime Anchor System.

**1. The "Dense Neighborhood" is Confirmed:**
The fact that *all tested systems*, including the inefficient "Random Even" search, achieved a **100% correction rate** provides the most powerful evidence possible for the **Prime Neighborhood Saturation Conjecture**. The neighborhood around a "messy" prime appears to be so saturated with fixes that a solution is *always* nearby, regardless of the search method's efficiency.

**2. The $S_n$ System is Obsolete (but was the Key):**
This is the final and most crucial finding. The $S_n$ system is **not** special or optimized.

[Test 10](r-max-efficiency.py) proves that a "Perfected $\pmod{210}$" system is **definitively superior** in every metric:
* It is **more efficient at $r=1$** (94.32% vs 75.85%).
* It has a **smaller overall search depth** ($r_{max}=10$ vs $r_{max}=16$).

This proves that the $S_n$ system's efficiency was simply that of a $\pmod{30}$-level filter. The "r_max Mystery" is solved: efficiency is not a unique property of the $S_n$ sequence, but a direct function of the **Primorial Filter's** strength.

The original "Prime Anchor System" ($S_n$) served its purpose as the prototype that led to this final discovery, and is now superseded by the understanding of the underlying Primorial Filter mechanism.

**3. The New Question: Optimal Efficiency ($r_{min}$ Conjecture):**
While the research confirms the 100% saturation of fixes, it opens a new question about the *optimal* efficiency of the correction mechanism. 

This can be framed as the **" $r_{min}$ Conjecture "**: <i>What is the theoretical minimum value $r_{min}$ such that there exists a deterministic anchor system guaranteeing a 100% correction rate with $r_{max} = r_{min}$? Does the "Perfected $\pmod{210}$" system, with its observed $r_{max}=10$, achieve this optimal efficiency?</i> This question about the true lower bound of $r_{max}$ represents the next frontier in understanding the structure revealed by this research. The research is therefore complete.
