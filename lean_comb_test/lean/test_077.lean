import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_077(n:ℕ): ∑ k ∈ Finset.Ico 1 (2*n),(-1:ℝ)^(k-1)*1/(Nat.choose (2*n) k)=1/(n+1)      := sorry
