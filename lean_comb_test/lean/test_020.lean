import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_020 (n m r : ℕ) :
    ∑ k ∈ range (n + 1), (-1 : ℝ) ^ k * choose n k * choose (m - k) r = choose (m - n) (r - n)       := sorry
