program situational_constraint_neglect
  implicit none

  integer, parameter :: n = 1000
  integer :: i
  real :: constraint, load, accountability, perspective
  real :: perceived, disposition, situation
  real :: fae_sum, neglect_sum
  real :: u1, u2, u3, u4

  call random_seed()
  fae_sum = 0.0
  neglect_sum = 0.0

  do i = 1, n
     call random_number(u1)
     call random_number(u2)
     call random_number(u3)
     call random_number(u4)

     constraint = 10.0 * u1
     load = 10.0 * u2
     accountability = 10.0 * u3
     perspective = 10.0 * u4

     perceived = max(0.0, min(10.0, constraint - 0.30 * load + 0.30 * accountability + 0.25 * perspective))
     disposition = max(0.0, min(10.0, 5.0 + 0.35 * load - 0.30 * perceived - 0.20 * accountability))
     situation = max(0.0, min(10.0, 3.0 + 0.50 * perceived + 0.25 * accountability + 0.25 * perspective - 0.20 * load))

     fae_sum = fae_sum + disposition - situation
     neglect_sum = neglect_sum + constraint - perceived
  end do

  print *, "Situational constraint neglect model"
  print *, "Mean FAE score: ", fae_sum / n
  print *, "Mean constraint neglect: ", neglect_sum / n
end program situational_constraint_neglect
