program contribution_probability_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i
  real :: trust, norm, enforcement, legitimacy, reciprocity, p, u
  real :: contribution_sum, free_ride_sum, endowment

  call random_seed()
  contribution_sum = 0.0
  free_ride_sum = 0.0
  endowment = 20.0

  do i = 1, n
     call random_number(u)
     trust = 10.0 * u
     call random_number(u)
     norm = 10.0 * u
     call random_number(u)
     enforcement = 10.0 * u
     call random_number(u)
     legitimacy = 10.0 * u
     call random_number(u)
     reciprocity = 10.0 * u

     p = 1.0 / (1.0 + exp(-(-2.0 + 0.25 * trust + 0.24 * norm + 0.17 * enforcement + 0.22 * legitimacy + 0.18 * reciprocity)))
     contribution_sum = contribution_sum + endowment * p
     free_ride_sum = free_ride_sum + (endowment - endowment * p) / endowment
  end do

  print *, "Contribution probability model"
  print *, "Trials: ", n
  print *, "Mean contribution: ", contribution_sum / n
  print *, "Mean free-riding index: ", free_ride_sum / n
end program contribution_probability_model
