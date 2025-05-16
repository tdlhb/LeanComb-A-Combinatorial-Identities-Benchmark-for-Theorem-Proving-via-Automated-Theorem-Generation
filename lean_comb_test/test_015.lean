import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_015 (n : ℕ) (h : n > 0) :
    ∑ k in Finset.range (n + 1), Nat.choose (2 * n) (2 * k + 1) = 2 ^ (2 * n - 1)    := sorry
