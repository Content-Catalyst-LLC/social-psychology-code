program bounded_rationality_recurrence
  implicit none

  integer, parameter :: steps = 60
  integer :: t
  real :: cognitive_effort, accuracy, effort_cost, net_utility

  cognitive_effort = 0.30
  effort_cost = 0.40

  print *, "step,cognitive_effort,accuracy,net_utility"

  do t = 1, steps
     cognitive_effort = cognitive_effort + 0.02
     if (cognitive_effort > 1.0) cognitive_effort = 1.0

     accuracy = 1.0 - exp(-3.0 * cognitive_effort)
     net_utility = accuracy - effort_cost * cognitive_effort

     print *, t, cognitive_effort, accuracy, net_utility
  end do
end program bounded_rationality_recurrence
