import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_034(n:ℕ)(x:ℝ):∑ i in Finset.range (n+1),(Nat.choose n i)^2*x^i=∑ i in Finset.range (n+1),Nat.choose n i *Nat.choose (2*n-i) n*(x-1)^i      := sorry
