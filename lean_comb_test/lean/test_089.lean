import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_089 (n m r : ℕ) :
    ∑ k in range (n + 1), choose m k * choose r (n - k) = choose (m + r) n       := sorry
