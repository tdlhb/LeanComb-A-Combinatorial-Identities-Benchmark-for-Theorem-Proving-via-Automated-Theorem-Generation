import Mathlib
import Theorem
open Nat Finset BigOperators Real

theorem test_080 (x : ℝ) (k : ℕ) :
  ∑' n : Set.Ici k, deriv (fun (x:ℝ) => (choose n k) * (x ^ (n : ℕ))) x
  =  ∑' n : Set.Ici k, (choose n k) * n * (x ^ ((n-1) : ℕ))        := sorry
