import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_022 (n : ℕ):
  ∑ k in Finset.range (n + 1), 1 / (((k : ℝ) + 1) * (k + 2)) * Nat.choose n k
  = (2 ^ (n + 2) - n - 3) / (((n : ℝ) + 1) * (n + 2))         := sorry
