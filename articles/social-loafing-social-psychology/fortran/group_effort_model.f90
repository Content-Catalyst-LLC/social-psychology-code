program group_effort_model
  implicit none
  integer :: n
  real :: coord, motiv, effort
  print *, "group_size,per_person_effort,total_output,motivation_loss,coordination_loss"
  do n = 1, 12
     coord = 2.0 * log(1.0 + real(n))
     motiv = 4.0 * log(1.0 + real(n))
     effort = 100.0 - coord - motiv
     if (effort < 0.0) effort = 0.0
     print *, n, effort, real(n)*effort, motiv, coord
  end do
end program group_effort_model
