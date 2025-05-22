import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_064 (n : ℕ) (hn : 1 ≤ n):
    ∑ k in Finset.range (n / 2 + 1), (-1 : ℝ) ^ k * (n / (n - k)) * (Nat.choose (n - k) k) * 2 ^ (n - 2 * k) = 2        := sorry
