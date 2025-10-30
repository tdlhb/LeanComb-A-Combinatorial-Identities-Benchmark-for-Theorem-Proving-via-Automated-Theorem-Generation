import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_076 (r : ℕ ) (n : ℕ) (hrn : r > n) : Nat.choose (r + (n - r) - 1) (n - r) = Nat.choose (n - 1) (n - r)  := sorry
