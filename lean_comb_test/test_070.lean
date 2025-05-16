import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_070 (n : ℕ) (hn : 1 ≤ n):
    ∑ k in range (n + 1), choose (2 * n) k = 2 ^ (2 * n - 1) + (1 / 2 : ℝ) * choose (2 * n) n       := sorry
