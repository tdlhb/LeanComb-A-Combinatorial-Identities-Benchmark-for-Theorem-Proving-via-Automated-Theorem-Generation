import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_013 (n : ℕ) :
  ∑ k ∈ Finset.range (n + 1), ((k + 1) ^ 2 * Nat.choose n k : ℝ) = (2 : ℝ) ^ (n - 2) * (n ^ 2 + 5 * n + 4)   := sorry
