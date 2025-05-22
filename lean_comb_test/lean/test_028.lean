import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_028(n:ℕ)(hn:n≥ 1):∑ k ∈ Finset.Ico 1 (n+1),1/k*Nat.choose (2*(k-1)) (k-1) *Nat.choose (2*(n-k)) (n-k)=1/2*Nat.choose (2*n) n        := sorry
