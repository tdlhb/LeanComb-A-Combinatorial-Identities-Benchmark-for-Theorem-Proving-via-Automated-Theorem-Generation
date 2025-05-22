import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_039 (n m : ℕ) :
    ∑ k in range (n + 1), choose (m - k) (n - k) = choose (m + 1) n       := sorry
