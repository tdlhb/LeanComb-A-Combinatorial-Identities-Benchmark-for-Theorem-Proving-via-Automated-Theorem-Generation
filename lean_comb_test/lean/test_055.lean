import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_055 (n : ℕ) (x : ℝ) :
  ∑ k in range (n + 1), (-1) ^ k * choose n k * (x - k) ^ (n + 1)
  = (x - n / 2) * (n + 1) !       := sorry
