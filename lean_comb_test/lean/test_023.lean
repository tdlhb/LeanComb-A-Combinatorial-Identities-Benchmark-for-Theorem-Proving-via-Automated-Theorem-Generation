import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_023 (n : ℕ) :
  ∑ k in Finset.range (n + 1),((k : ℝ) + 2) / (k + 1) * Nat.choose n k
  = (((n : ℝ) + 3) * 2 ^ n - 1) / (n + 1)         := sorry
