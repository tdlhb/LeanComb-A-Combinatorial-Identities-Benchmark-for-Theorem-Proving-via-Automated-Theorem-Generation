import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_046 (n m : ℕ)(h : m ≥ 2 * n) (hn : 1 ≤ n):
    ∑ k in range (n + 1), (-1 : ℝ) ^ k * Nat.choose n k * Nat.choose (m - 2 * k) (n - 1) = 0       := sorry
