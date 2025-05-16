import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_026(n m:ℕ)(hnm:m≤n):
  Nat.choose (n+r-1) r=∑ k in Finset.range (m+1),Nat.choose (m+k+1) k *Nat.choose (n-m+r-k-1) (r-k)         := sorry
