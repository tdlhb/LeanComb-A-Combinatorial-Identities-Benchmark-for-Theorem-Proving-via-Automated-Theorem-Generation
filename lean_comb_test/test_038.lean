import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_038 (n : ℕ) (hn : 1 ≤ n):
    ∑ k in range (n + 1), (4 * n).choose (4 * k) =
      (1 / 4 : ℝ) * (2 ^ (4 * n) + (-1) ^ n * 2 ^ (2 * n + 1))       := sorry
