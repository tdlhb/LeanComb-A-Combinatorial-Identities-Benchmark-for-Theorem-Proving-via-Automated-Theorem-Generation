import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_084 (n k:ℕ)(hn:n≥3)(hk:k≥1):
  Nat.choose n k - Nat.choose (n-3) k=Nat.choose (n-1) (k-1) +Nat.choose (n-2) (k-1)+Nat.choose (n-3) (k-1)      := sorry
