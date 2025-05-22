import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_031 (n m :ℕ) : ∑ k in Finset.range (n+1), Nat.choose m k  * Nat.choose (m+n-1) k = (m+n)/n       := sorry
