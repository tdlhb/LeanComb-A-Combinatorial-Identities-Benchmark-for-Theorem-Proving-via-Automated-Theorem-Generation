import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_027(n:ℕ)(hn:n≥ 1):∑ k in Finset.range (n+1),k*(Nat.choose n k)^2=n*Nat.choose (2*n-1) (n-1)        := sorry
