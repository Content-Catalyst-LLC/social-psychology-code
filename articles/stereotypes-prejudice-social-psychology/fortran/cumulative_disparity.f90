program cumulative_disparity
  implicit none

  integer, parameter :: decisions = 1000
  integer :: t
  real :: inequality, decision_disparity

  inequality = 0.0

  print *, "decision,decision_disparity,cumulative_inequality"

  do t = 1, decisions
     decision_disparity = 0.015
     inequality = inequality + decision_disparity
     if (mod(t, 50) == 0) then
        print *, t, decision_disparity, inequality
     end if
  end do
end program cumulative_disparity
