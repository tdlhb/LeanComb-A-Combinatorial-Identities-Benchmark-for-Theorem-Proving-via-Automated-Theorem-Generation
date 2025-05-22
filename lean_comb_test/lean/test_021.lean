import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_021 (n r : ℕ) (hn : 0 < n) (hrn : r ≤ n - 1) :
  Nat.choose n r = (n : ℝ) / (n - r) * Nat.choose (n - 1) r         := sorry
