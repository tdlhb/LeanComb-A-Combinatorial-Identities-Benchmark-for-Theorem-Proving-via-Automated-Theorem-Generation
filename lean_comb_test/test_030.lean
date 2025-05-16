import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_030(n:ℕ):∑ k in Finset.range (n + 1),2^(n-k)*Nat.choose (n+k) (2*k)=(2^(2*n+1)+1)/3        := sorry
