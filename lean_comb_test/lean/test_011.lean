import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_011 {n : ℕ} : ∑ k ∈ Finset.range (n + 1),
  (-1 : ℝ) ^ (n - k) * 2 ^ (2 * k) * Nat.choose (n + k + 1) (2 * k + 1)= n + 1   := sorry
