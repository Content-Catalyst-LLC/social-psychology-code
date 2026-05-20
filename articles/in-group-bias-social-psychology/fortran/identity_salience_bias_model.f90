program identity_salience_bias_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i, ingroup
  real :: identity, threat, norm, bias_force, allocation
  real :: ing_sum, out_sum
  integer :: ing_n, out_n
  real :: u1, u2, u3, u4

  call random_seed()
  ing_sum = 0.0
  out_sum = 0.0
  ing_n = 0
  out_n = 0

  do i = 1, n
     call random_number(u1)
     call random_number(u2)
     call random_number(u3)
     call random_number(u4)

     ingroup = merge(1, 0, u1 < 0.5)
     identity = 10.0 * u2
     threat = 10.0 * u3
     norm = 10.0 * u4

     if (ingroup == 1) then
        bias_force = 0.30 * identity + 0.22 * threat + 0.18 * norm
        allocation = max(0.0, min(100.0, 50.0 + 4.5 * bias_force))
        ing_sum = ing_sum + allocation
        ing_n = ing_n + 1
     else
        bias_force = -0.12 * threat
        allocation = max(0.0, min(100.0, 50.0 + 4.5 * bias_force))
        out_sum = out_sum + allocation
        out_n = out_n + 1
     end if
  end do

  print *, "Identity salience favoritism simulation"
  print *, "Mean ingroup allocation: ", ing_sum / ing_n
  print *, "Mean outgroup allocation: ", out_sum / out_n
  print *, "Allocation differential: ", ing_sum / ing_n - out_sum / out_n
end program identity_salience_bias_model
