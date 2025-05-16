import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_065 (n m r : ℕ) :
    ∑ k in range (n + 1), choose n k * choose m (k + r) = choose (n + m) (n + r)       := sorry
