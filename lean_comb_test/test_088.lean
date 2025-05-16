import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_088 {n k s : ℕ} (hkn : k ≤ n) (hsk : s + 1 ≤ k) :
    n.choose k * k.choose (s + 1) = n.choose (s + 1) * (n - s - 1).choose (k - s - 1)       := sorry
