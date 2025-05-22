import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_040 (n : ℕ) (hn : 1 ≤ n):
  ∑ k in Finset.range (n + 1), ∑ l in Finset.range (k + 1), (-1 : ℝ) ^ l * Nat.choose k l * (l + 1) ^ n = 0        := sorry
