import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_044 (n : ℕ) :
    ∑ k in range n, (-1 : ℝ) ^ k * (cos (k * π / n)) ^ n =
      n / 2 ^ (n - 1)        := sorry
