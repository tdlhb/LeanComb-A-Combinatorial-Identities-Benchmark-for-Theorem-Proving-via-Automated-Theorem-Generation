import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_036 (n : ℕ) :
    ∑ k in range (n + 1), (-1 : ℝ) ^ k * Nat.choose n k * 2 ^ (2 * k) * (Nat.choose (2 * k) k : ℝ)⁻¹ =
      1 / (1 - 2 * n)       := sorry
