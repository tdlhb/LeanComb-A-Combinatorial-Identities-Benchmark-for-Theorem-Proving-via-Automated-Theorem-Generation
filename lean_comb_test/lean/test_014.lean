import Mathlib
import Theorem
open BigOperators Nat Finset Real

theorem test_014 (n:ℕ):∑ k in Finset.range (n+1),1/((k+1)*(k+3))*Nat.choose n k=(2^(n+3)-n-4)/(2*(n+2)*(n+3))   := sorry
