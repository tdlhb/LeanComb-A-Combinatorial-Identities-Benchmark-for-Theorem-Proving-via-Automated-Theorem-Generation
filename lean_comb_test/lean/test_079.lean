import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_079 (n m:ℕ):∑ k in Finset.range (m+1),Nat.choose (n+k+1) k =Nat.choose (n+m+2) m      := sorry
