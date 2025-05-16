import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_062 (n : ℕ) (x : ℝ):
    ∑ k ∈ Finset.range (n + 1), (-1 : ℝ) ^ k * Nat.choose n k * (∑ k ∈ Finset.range (n + 1), (x ^ k) / k) =
    ((-1 : ℝ) / n) * (1 - (1 - x) ^ n)        := sorry
