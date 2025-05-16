import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_063 (n p: ℕ) (x : ℝ) :
    ∑ k ∈ Finset.range (n + 1), (-1 : ℝ) ^ k * Nat.choose (n + p) (k + p) =
     Nat.choose (n + p - 1) n        := sorry
