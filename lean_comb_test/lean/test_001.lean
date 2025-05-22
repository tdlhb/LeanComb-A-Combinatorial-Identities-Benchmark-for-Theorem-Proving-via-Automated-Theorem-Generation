import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_001 {n : ℕ} : ∑ k ∈ Finset.range (n + 1), ((-1) ^ k * k * stirling_first n k : ℝ) = (-1 : ℝ)^n * (2^n - 1)   := sorry
