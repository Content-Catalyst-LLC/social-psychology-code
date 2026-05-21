program coherence_pressure_recurrence
  implicit none

  integer, parameter :: steps = 60
  integer :: t
  real :: attitude, pressure, affirmation, justification

  attitude = 20.0
  pressure = 0.65
  affirmation = 0.20
  justification = 0.15

  print *, "step,attitude"

  do t = 1, steps
     attitude = attitude + 2.0 * pressure - 1.1 * affirmation - 0.9 * justification
     if (attitude > 100.0) attitude = 100.0
     if (attitude < -100.0) attitude = -100.0
     print *, t, attitude
  end do
end program coherence_pressure_recurrence
