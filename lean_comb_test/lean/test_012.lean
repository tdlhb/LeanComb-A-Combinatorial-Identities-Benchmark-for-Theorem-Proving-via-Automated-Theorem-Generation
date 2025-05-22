import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_012 {n : ℕ} :
    catalan n = choose (2 * n) n - choose (2 * n) (n - 1)   := sorry
