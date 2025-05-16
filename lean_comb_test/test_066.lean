import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_066 (n m : ℕ) :
    ∑ k in range (n + 1), choose n k * choose m k * k = n * choose (n + m - 1) n       := sorry
