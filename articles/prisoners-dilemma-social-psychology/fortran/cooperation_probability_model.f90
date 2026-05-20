program cooperation_probability_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i, cooperation_count
  real :: trust, expected_partner, reputation, enforcement, temptation_gap, p, u
  real :: p_sum

  call random_seed()
  cooperation_count = 0
  p_sum = 0.0

  do i = 1, n
     call random_number(u)
     trust = 10.0 * u
     call random_number(u)
     expected_partner = 10.0 * u
     call random_number(u)
     reputation = 10.0 * u
     call random_number(u)
     enforcement = 10.0 * u

     temptation_gap = 2.0 - 0.25 * enforcement
     p = 1.0 / (1.0 + exp(-(-3.0 + 0.35 * trust + 0.30 * expected_partner + 0.18 * reputation + 0.16 * enforcement - 0.55 * temptation_gap)))

     call random_number(u)
     if (u < p) cooperation_count = cooperation_count + 1
     p_sum = p_sum + p
  end do

  print *, "Cooperation probability model"
  print *, "Trials: ", n
  print *, "Mean cooperation probability: ", p_sum / n
  print *, "Observed cooperation rate: ", real(cooperation_count) / real(n)
end program cooperation_probability_model
