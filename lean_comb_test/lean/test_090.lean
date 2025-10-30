import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_090 (k : ℕ) (r : ℕ) (h₁ : r ≤ r+k-1) (h₂ : k ≥ 1): Nat.choose (r + k - 1) r = Nat.choose (r + k - 1) (k - 1)         := sorry
