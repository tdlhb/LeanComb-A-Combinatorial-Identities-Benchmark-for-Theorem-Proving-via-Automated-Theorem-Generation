import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_047 (n : ℕ) :
    ∑ k in Finset.range (n + 1), Nat.choose (2 * n) k = 2 ^ (n - 1) + (Nat.choose (2 * n) n) / 2        := sorry
