import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_048 (n m k : ℕ)(hmk : m ≤ k) (hkn : k ≤ n) :
    Nat.choose n k * Nat.choose k m = Nat.choose n (k - m) * Nat.choose (n - k + m) m        := sorry
