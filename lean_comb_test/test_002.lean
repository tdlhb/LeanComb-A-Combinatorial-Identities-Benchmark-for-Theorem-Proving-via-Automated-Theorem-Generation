import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_002 {n : ℕ} : ∑ k ∈ range (n + 1),
  ((Nat.choose (2 * n) (n + k)) ^ 2 / (Nat.choose (2 * n + 2 * k) (n + k)) ^ 2 : ℝ) *
    ((4 * k + 1) * 2 ^ (4 * k) / (2 * n + 2 * k + 1) ^ 2 : ℝ) = 1 / (4 * n + 1)   := sorry
