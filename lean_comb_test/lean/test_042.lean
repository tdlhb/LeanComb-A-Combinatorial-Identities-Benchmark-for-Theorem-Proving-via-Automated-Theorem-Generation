import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_042 (n : ℕ) :
    ∑ k in Finset.range (n / 2 + 1), ((n + 1 - 2 * k) ^ 2) / (n + 1 - k) * Nat.choose n k = 2 ^ n       := sorry
