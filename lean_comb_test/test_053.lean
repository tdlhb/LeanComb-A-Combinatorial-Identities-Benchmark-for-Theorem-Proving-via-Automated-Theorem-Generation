import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_053 (n : ℕ) (x : ℝ) :
  ∑ k in range (n + 1), (-1) ^ k * choose n k * (x + n - k) ^ n
  = n !       := sorry
