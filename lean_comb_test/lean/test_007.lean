import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_007  {x : ℝ} (hx : |x| < 1) :
    Real.log (1 + x) = ∑' k : ℕ, (-1 : ℝ)^k * k * x^(k + 1) / (k + 1)   := sorry
