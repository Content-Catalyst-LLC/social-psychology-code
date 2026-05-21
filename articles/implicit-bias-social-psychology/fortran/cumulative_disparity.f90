program cumulative_disparity
  implicit none

  integer, parameter :: decisions = 1000
  integer :: t
  real :: cumulative, bias

  cumulative = 0.0
  print *, "decision,bias_contribution,cumulative_disparity"

  do t = 1, decisions
     bias = 0.012
     cumulative = cumulative + bias
     if (mod(t, 50) == 0) then
        print *, t, bias, cumulative
     end if
  end do
end program cumulative_disparity
