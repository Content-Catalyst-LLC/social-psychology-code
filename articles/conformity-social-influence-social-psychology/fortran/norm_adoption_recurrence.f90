program norm_adoption_recurrence
  implicit none

  integer, parameter :: steps = 25
  integer :: t
  real :: private_judgment, group_consensus, lambda, dissent, judgment

  private_judgment = 0.20
  group_consensus = 1.00
  lambda = 0.32
  dissent = 0.10
  judgment = private_judgment

  print *, "step,private_judgment,group_consensus,lambda,dissent,updated_judgment"

  do t = 1, steps
     judgment = (1.0 - lambda) * judgment + lambda * group_consensus - 0.15 * dissent
     print *, t, private_judgment, group_consensus, lambda, dissent, judgment
  end do
end program norm_adoption_recurrence
