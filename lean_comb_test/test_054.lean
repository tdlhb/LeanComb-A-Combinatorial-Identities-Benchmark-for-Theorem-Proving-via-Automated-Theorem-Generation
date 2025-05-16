import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_054 (n : ℕ) :
    ∑ k in Finset.range (n + 1), (-1 : ℝ) ^ k * 2 ^ (2 * n - 2 * k) * Nat.choose (2 * n - k) k = 2 * n + 1        := sorry
