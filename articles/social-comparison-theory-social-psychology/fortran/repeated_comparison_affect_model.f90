program repeated_comparison_affect_model
  implicit none

  integer, parameter :: n = 1000
  integer, parameter :: days = 30
  integer :: i, d
  real :: self_eval, orientation, exposure, upward_gap, attainability
  real :: inspiration, discouragement
  real :: final_sum
  real :: u1, u2, u3

  call random_seed()
  final_sum = 0.0

  do i = 1, n
     call random_number(u1)
     call random_number(u2)
     self_eval = 4.5 + 2.5 * u1
     orientation = 10.0 * u2

     do d = 1, days
        call random_number(u1)
        call random_number(u2)
        call random_number(u3)
        exposure = 10.0 * u1
        upward_gap = max(0.0, 2.0 + 0.20 * exposure + (u2 - 0.5) * 2.0)
        attainability = max(0.0, min(10.0, 5.0 - 0.25 * exposure + (u3 - 0.5) * 2.0))
        inspiration = max(0.0, min(10.0, 0.30 * upward_gap * attainability / 10.0))
        discouragement = max(0.0, min(10.0, 0.28 * upward_gap * max(0.0, 5.0 - attainability) / 5.0))
        self_eval = max(0.0, min(10.0, self_eval - 0.04 * upward_gap * orientation / 10.0 + 0.05 * inspiration - 0.05 * discouragement))
     end do

     final_sum = final_sum + self_eval
  end do

  print *, "Repeated social-comparison affect model"
  print *, "Participants: ", n
  print *, "Days: ", days
  print *, "Mean final self-evaluation: ", final_sum / n
end program repeated_comparison_affect_model
