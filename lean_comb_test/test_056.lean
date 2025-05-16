import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_056 (n m : ℕ) (hn : 1 ≤ n):
    ∑ k in Finset.range (m + 1), Nat.choose (k + n - 1) (n - 1) = Nat.choose (n + m) n        := sorry
