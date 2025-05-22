import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_037 (n : ℕ) (hn : n ≥ 4) :
  ∑ k in Finset.range (n + 1), k ^ 4 * Nat.choose n k =
    Nat.choose n 1 * 2 ^ (n - 1) + 14 * Nat.choose n 2 * 2 ^ (n - 2) +
    36 * Nat.choose n 3 * 2 ^ (n - 3) + 24 * Nat.choose n 4 * 2 ^ (n - 4)        := sorry
