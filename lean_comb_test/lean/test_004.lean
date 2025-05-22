import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_004 {x : ℝ} {n : ℕ} : ∑ k ∈ range (n + 1), ((-1) ^ k * Nat.choose n k * Nat.choose (2 * k) (n + k) * x ^ k : ℝ) = 2 ^ n * Nat.choose (2 * n) n   := sorry
