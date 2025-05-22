import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_025(n:ℕ) : ∑ k ∈ Finset.Ico 1 (n+1),k^2*Nat.choose n k=n*(n+1)*2^(n-2)         := sorry
