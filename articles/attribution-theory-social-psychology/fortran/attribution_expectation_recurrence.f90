program attribution_expectation_recurrence
  implicit none

  integer, parameter :: steps = 60
  integer :: t
  real :: expectation, stability, learning_rate

  expectation = 50.0
  stability = 0.75
  learning_rate = 0.18

  print *, "step,achievement_expectation"

  do t = 1, steps
     expectation = expectation + learning_rate * ((100.0 * stability) - expectation)
     if (expectation > 100.0) expectation = 100.0
     if (expectation < 0.0) expectation = 0.0
     print *, t, expectation
  end do
end program attribution_expectation_recurrence
