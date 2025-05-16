import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_091(n:ℕ) : 2^n = ∑ k in Finset.range (n+1),(-1:ℝ)^k*Nat.choose n k *3^(n-k)         := sorry
