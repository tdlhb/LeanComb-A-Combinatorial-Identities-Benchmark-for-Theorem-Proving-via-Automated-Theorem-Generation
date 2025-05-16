import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_076 (n m k : ℕ) :
    ∑ r in range (k + 1), choose n r * choose m (k - r) = choose (n + m) k       := sorry
