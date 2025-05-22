import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_068 (n : ℕ) :
    ∑ k in range (n + 1), (-1 : ℝ) ^ k * choose n k * 10 ^ k = (-9 : ℝ) ^ n       := sorry
