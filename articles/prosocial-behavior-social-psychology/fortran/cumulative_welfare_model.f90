program cumulative_welfare_model
  implicit none

  integer, parameter :: periods = 20
  integer :: t
  real :: welfare, contributions, depletion

  welfare = 100.0
  print *, "period,welfare,contributions,depletion"

  do t = 1, periods
     contributions = 5.0 + 0.1 * welfare
     depletion = 8.0
     welfare = welfare + contributions - depletion
     print *, t, welfare, contributions, depletion
  end do
end program cumulative_welfare_model
