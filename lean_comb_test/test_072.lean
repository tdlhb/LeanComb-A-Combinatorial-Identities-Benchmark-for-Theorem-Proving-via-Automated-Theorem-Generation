import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_072 (n m s : ℕ) :
    ∑ k in range s, choose k n * choose (k + m) m = choose s n * choose (s + m) m * (s - n) / (m + n + 1 : ℝ)       := sorry
