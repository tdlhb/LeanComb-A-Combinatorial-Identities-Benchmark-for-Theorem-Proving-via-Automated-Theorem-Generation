import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_082 (n : ℕ) :
    ∑ k in Finset.range (n + 1), 2 ^ k * Nat.choose n k = 3 ^ n        := sorry
