import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_016 (n : ℕ) (x : ℝ) :
    ∑ k in range (n + 1), (-1 : ℝ) ^ k * (n.choose k) * 2 ^ k * (cos (x / 2)) ^ k * cos ((k / 2) * x) =
      (-1 : ℝ) ^ n * cos (n * x)     := sorry
