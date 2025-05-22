import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_024 (n : ℕ) :
  ∑ k in Finset.range (n + 1), (-1 : ℝ) ^ k * 1 / (n+k+1) * Nat.choose n k = (n !) ^ 2 / (2 * n + 1) !         := sorry
