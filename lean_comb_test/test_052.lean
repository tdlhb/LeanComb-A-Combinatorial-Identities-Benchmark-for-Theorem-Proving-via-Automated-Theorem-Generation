import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_052 (n m : ℕ) (hmn : 0 < m ∨ 0 < n) :
    ∑ k in Finset.range (n + 1), (-1 : ℝ) ^ k * (Nat.choose n k ) * (m / (m + k)) =
    1 / (Nat.choose (m + n) n : ℝ)        := sorry
