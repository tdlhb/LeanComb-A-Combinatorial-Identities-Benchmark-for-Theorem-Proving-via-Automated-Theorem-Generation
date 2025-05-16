import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_057 (n : ℕ) (hn : n ≥ 2) :
    ∑ k in Finset.range (n - 1), Nat.choose n k = 2 ^ (n - 1)        := sorry
