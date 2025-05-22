import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_071 (n : ℕ) :
    ∑ k in range (n + 1), ((k : ℝ) + 1) ^ 2 * choose n k = (2 : ℝ) ^ ((n : ℝ) - 2) * (n ^ 2 + 5 * n + 4)       := sorry
