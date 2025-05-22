import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_017 (n : ℕ) (hn : 4 ≤ n) :
    stirling_second n (n - 2) = n.choose 3 + 3 * n.choose 4    := sorry
