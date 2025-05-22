import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_067 (n m r : ℕ) :
    ∑ k in range (n + 1), (-1 : ℝ) ^ k * choose n k * choose (m + k) (r + k) = (-1 : ℝ) ^ n * choose m (n + r)       := sorry
