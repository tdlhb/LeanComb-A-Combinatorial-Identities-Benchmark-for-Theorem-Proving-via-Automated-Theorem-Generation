import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_005 {n : ℕ} : ∑ k ∈ range (n + 1),((-1) ^ k * Nat.choose n k  * k * 2 ^ k : ℝ) = 2 * n * (-1 : ℝ) ^ n  := sorry
