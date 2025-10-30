import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_071 (n:ℕ) (hn : n ≥ 4) :Nat.choose n 3 - (n - 2) ^ 2 - (n - 4) =n * (Nat.choose (n - 4) 2) / 3     := sorry
