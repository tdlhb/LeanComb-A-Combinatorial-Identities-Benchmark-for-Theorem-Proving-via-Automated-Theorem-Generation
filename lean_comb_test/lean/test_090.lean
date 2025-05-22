import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_090(n:ℕ) : 3^n = ∑ k in Finset.range (n+1), Nat.choose n k *2^k         := sorry
