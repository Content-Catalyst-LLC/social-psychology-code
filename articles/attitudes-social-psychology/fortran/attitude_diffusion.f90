program attitude_diffusion
  implicit none

  integer :: t
  real :: attitude
  real, parameter :: norm_signal = 0.8
  real, parameter :: influence = 0.15

  attitude = 0.2

  print *, "Time", "Attitude"

  do t = 1, 10
     attitude = attitude + influence * (norm_signal - attitude)
     print *, t, attitude
  end do

end program attitude_diffusion
