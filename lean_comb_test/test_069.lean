import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_069 (n : ℕ) (hn : 2 < n) :
    ∑ k in range (n + 1), (-1 : ℝ) ^ k * k ^ 2 * choose n k = 0       := sorry
