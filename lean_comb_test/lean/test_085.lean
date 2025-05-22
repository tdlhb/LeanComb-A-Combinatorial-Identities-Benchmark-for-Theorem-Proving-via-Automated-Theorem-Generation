import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_085 (n k : ℕ) :
    n.ascFactorial (k + 1) = (k + 1) ! * (n + k).choose (k + 1)       := sorry
