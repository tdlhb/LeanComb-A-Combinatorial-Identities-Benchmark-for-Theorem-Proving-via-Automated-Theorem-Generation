import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_073 (x n : ℕ) :
    ∑ k in Finset.range (n + 1),(Nat.choose n k) ^ 2 * choose (x + k) (2 * n)=(Nat.choose x n) ^ 2      := sorry
