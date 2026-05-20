program harmful_choice_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i, j, harmful_count
  real :: md, empathy, guilt, visibility, pressure, p
  real :: md_sum, p_sum
  real :: u

  call random_seed()
  md_sum = 0.0
  p_sum = 0.0
  harmful_count = 0

  do i = 1, n
     md = 0.0
     do j = 1, 8
        call random_number(u)
        md = md + 10.0 * u
     end do
     md = md / 8.0

     call random_number(u)
     empathy = 10.0 * u
     call random_number(u)
     guilt = 10.0 * u
     call random_number(u)
     visibility = 10.0 * u
     call random_number(u)
     pressure = 10.0 * u

     p = 1.0 / (1.0 + exp(-(-4.0 + 0.45 * md + 0.20 * pressure - 0.25 * empathy - 0.20 * guilt - 0.15 * visibility)))
     call random_number(u)

     if (u < p) harmful_count = harmful_count + 1
     md_sum = md_sum + md
     p_sum = p_sum + p
  end do

  print *, "Harmful choice model"
  print *, "Trials: ", n
  print *, "Mean moral disengagement index: ", md_sum / n
  print *, "Mean harmful decision probability: ", p_sum / n
  print *, "Observed harmful decision rate: ", real(harmful_count) / real(n)
end program harmful_choice_model
