import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_049 (n : ℕ) (x : ℝ) (hn : 1 ≤ n):
    ∑ k in range (n / 2 + 1), (Nat.choose n (2 * k)) * sin (2 * k * x) =
      2 ^ (n - 1) * (sin (n * x / 2) * (cos (x / 2)) ^ n + sin ((x + π) / 2) * (cos ((x + π) / 2)) ^ n)        := sorry
