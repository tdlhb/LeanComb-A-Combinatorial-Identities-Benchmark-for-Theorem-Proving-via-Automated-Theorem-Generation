import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_059 (n : ℕ) :
    ∑ k ∈  Finset.range (n + 1), Nat.choose (n + k) (2 * k) * 2 ^ (n - k) =
    (1 / 3 : ℝ) * (2 ^ (2 * n + 1) + 1)       := sorry
