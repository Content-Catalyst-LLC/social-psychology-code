program regulation_weight_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i
  real :: u, anonymity, group_identity, norm_clarity, accountability
  real :: lambda_group, norm_congruence
  real :: lambda_sum, norm_sum

  call random_seed()
  lambda_sum = 0.0
  norm_sum = 0.0

  do i = 1, n
     call random_number(u)
     anonymity = 10.0 * u
     call random_number(u)
     group_identity = 10.0 * u
     call random_number(u)
     norm_clarity = 10.0 * u
     call random_number(u)
     accountability = 10.0 * u

     lambda_group = 1.0 / (1.0 + exp(-(-2.0 + 0.32 * anonymity + 0.30 * group_identity + 0.18 * norm_clarity - 0.20 * accountability)))
     norm_congruence = 2.0 + 7.0 * lambda_group
     if (norm_congruence > 10.0) norm_congruence = 10.0

     lambda_sum = lambda_sum + lambda_group
     norm_sum = norm_sum + norm_congruence
  end do

  print *, "Personal-versus-group regulation model"
  print *, "Trials: ", n
  print *, "Mean group-regulation weight: ", lambda_sum / real(n)
  print *, "Mean norm congruence: ", norm_sum / real(n)
end program regulation_weight_model
