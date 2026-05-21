program intervention_threshold_model
  implicit none

  integer, parameter :: max_bystanders = 50
  integer :: n
  real :: diffusion, responsibility, probability

  print *, "bystanders,diffusion_responsibility,felt_responsibility,helping_probability"

  do n = 0, max_bystanders
     diffusion = 1.0 + 1.25 * log(1.0 + real(n))
     if (diffusion > 10.0) diffusion = 10.0
     responsibility = 8.5 - 0.80 * diffusion
     if (responsibility < 0.0) responsibility = 0.0
     probability = 1.0 / (1.0 + exp(-(-3.5 + 0.55 * responsibility + 0.35 * 8.0 - 0.40 * diffusion)))

     print *, n, diffusion, responsibility, probability
  end do
end program intervention_threshold_model
