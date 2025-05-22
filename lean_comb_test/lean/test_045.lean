import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_045 (n k : ℕ)(hn : n > 0)(hk : k > 0) :
    (Nat.choose n k : ℝ) = (n : ℝ) / (k : ℝ) * Nat.choose (n - 1) (k - 1)       := sorry
