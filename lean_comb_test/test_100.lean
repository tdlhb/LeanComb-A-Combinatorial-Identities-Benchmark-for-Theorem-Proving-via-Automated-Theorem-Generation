import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_100 (n:ℕ) : ∑ m ∈ range (n + 1), (-1:ℝ) ^ m * 10 ^ (n- m) * n.choose m=9^n      := sorry
