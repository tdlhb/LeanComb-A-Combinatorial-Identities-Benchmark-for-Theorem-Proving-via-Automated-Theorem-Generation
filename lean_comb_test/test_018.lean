import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_018 (n : ℕ) (hn : 1 ≤ n):
  ∑ k ∈ Finset.range (n + 1), (-1 : ℝ) ^ k * (k + 1) ^ n * Nat.choose (n + 1) (k + 1) = 0    := sorry
