import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_095 (n : ℕ) :
    ∑ k in range (n + 1), (-1 : ℝ) ^ k * 1/ (Nat.choose n k) =
      (n + 1) / (n + 2) * (1 + (-1) ^ n)        := sorry
