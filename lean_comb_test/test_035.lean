import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_035(n k:ℕ)(hn:n≥1)(hr:r≥1):∑ r in Finset.range (n+2),Nat.choose (n+k-r) (k-1)=Nat.choose (n+k+1) k      := sorry
