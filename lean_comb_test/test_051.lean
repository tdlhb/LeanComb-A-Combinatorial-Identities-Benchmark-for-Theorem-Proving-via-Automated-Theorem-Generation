import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_051 (n : ℕ) :
    ∑ k in Finset.range (n / 2 + 1), Nat.choose (n - k) k * 2 ^ k =
    (1 / 3 : ℝ) * (2 ^(n + 1) + (-1 : ℝ) ^ n)        := sorry
