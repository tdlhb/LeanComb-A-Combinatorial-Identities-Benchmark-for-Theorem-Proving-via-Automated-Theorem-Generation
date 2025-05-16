import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_029 (n m:ℕ)(hn:n≥ 1) (h:n≥m): ∑ k in Finset.range (m+1),(-1:ℝ)^k * Nat.choose n k = (-1:ℝ)^m * Nat.choose (n-1) m         := sorry
