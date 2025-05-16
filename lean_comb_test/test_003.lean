import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_003 {n r : ℕ} : ∑ k ∈ range (n + 1), Nat.choose n k * Nat.choose k r * 2 ^ k = 2 ^ r * 3 ^ (n - r) * Nat.choose n r   := sorry
