import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_010 {n : ℕ} : ∑ k ∈ Finset.range (n + 1), k * (k !) = (n+1)! - 1   := sorry
