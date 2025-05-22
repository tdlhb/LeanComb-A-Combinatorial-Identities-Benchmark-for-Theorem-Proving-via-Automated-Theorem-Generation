import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_093 (n : ℕ) :
    ∑ k in Finset.range (n / 2 + 1), (-1 : ℝ) ^ k * Nat.choose (n - k ) k =(2 / Real.sqrt 3) *  Real.sin ((n + 1) * Real.pi / 3)        := sorry
