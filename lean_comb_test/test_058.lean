import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_058 (n : ℕ) :
    ∑ k ∈ Ico 1 (n + 1), ((-1 : ℝ) ^ (k - 1) * (2 ^ (2 * k : ℝ) / (2 * k - 1 : ℝ)) * (Nat.choose n k : ℝ) / (Nat.choose (2 * k - 2) (k - 1)  : ℝ))=
     4 * ∑ k in Finset.range n, (1 / (2 * k + 1))        := sorry
