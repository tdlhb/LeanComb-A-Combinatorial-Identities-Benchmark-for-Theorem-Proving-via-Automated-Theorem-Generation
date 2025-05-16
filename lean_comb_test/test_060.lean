import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_060 (n : ℕ) :
    ∑ k in range (n + 1), (-1 : ℝ) ^ k / (2 * k + 1) * Nat.choose n k * (Nat.choose (2 * k) k : ℝ)⁻¹ * 2 ^ (2 * k) =
      1 / (2 * n + 1)        := sorry
