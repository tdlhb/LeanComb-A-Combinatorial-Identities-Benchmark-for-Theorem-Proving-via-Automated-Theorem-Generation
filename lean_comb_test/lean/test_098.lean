import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_098 (n : ℕ) :
    ∑ k in Finset.range (n / 2 + 1), Nat.choose (n - k) k =
    (1 / Real.sqrt 5) * ( ((1 + Real.sqrt 5) / 2) ^ (n + 1) - ((1 - Real.sqrt 5) / 2) ^ (n + 1) )        := sorry
