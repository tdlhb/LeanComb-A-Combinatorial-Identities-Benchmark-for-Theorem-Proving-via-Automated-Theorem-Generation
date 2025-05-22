import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_041 (n : ℕ) (x : ℝ):
    ∑ k in Finset.range (n + 1), (-1 : ℝ) ^ k / (k + 1) * Nat.choose n k * ((1 + x) ^ (k + 1) - 1) =
    (-1) ^ n * x ^ (n + 1) / (n + 1)        := sorry
