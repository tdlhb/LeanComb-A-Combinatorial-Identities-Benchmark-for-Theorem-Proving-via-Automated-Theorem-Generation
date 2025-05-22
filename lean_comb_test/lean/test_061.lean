import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_061 (n : ℕ) :
    ∑ k in Finset.range (n + 1), (-1 : ℝ) ^ k * 2 ^ (2 * n - 2 * k) * Nat.choose (2 * n - k + 1) k = n + 1        := sorry
