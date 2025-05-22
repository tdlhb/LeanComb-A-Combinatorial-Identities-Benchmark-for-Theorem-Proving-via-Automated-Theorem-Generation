import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_099 (n k : ℕ) (hk : 1 < k) :
    choose (n + 1) (k - 1) = choose n (k - 2) + choose n (k - 1)       := sorry
