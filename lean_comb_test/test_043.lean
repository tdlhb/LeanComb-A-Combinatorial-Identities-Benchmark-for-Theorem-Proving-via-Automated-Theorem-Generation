import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_043 (n : ℕ) :
  ∑ k in range (n + 1), (-1 : ℝ) ^ k * choose n k * (∑ l in range k, (1 / l ^ 2 : ℝ))
  = -1 / n * ∑ k in range (n + 1), 1 / k        := sorry
