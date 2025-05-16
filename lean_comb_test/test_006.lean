import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_006 {n : ℕ} :
    Real.log 2 = ∑' k : ℕ, (-1 : ℝ)^(k - 1) / k.succ   := sorry
