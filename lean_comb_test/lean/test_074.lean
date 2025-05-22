import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_074 (x:ℝ)(n:ℕ):(x-1)^n=∑ k in Finset.range (n+1),Nat.choose n k *x^k*(-1:ℝ )^(n-k)      := sorry
