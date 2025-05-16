import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_050 (n : ℕ) :
    ∑ k in Finset.range (n / 2 + 1), Nat.choose (n - k) k * 6 ^ k =
    (1 / 5) * (3 ^ (n + 1) + (-1 : ℝ) ^ n * 2 ^ (n + 1))        := sorry
