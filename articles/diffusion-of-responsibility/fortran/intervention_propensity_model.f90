program intervention_propensity_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i, bystanders, interventions
  real :: ambiguity, evaluation, role, efficacy, concern, responsibility, p, u
  real :: responsibility_sum, probability_sum

  call random_seed()
  responsibility_sum = 0.0
  probability_sum = 0.0
  interventions = 0

  do i = 1, n
     call random_number(u)
     bystanders = int(12.0 * u)
     call random_number(u)
     ambiguity = 10.0 * u
     call random_number(u)
     evaluation = 10.0 * u
     call random_number(u)
     role = 10.0 * u
     call random_number(u)
     efficacy = 10.0 * u
     call random_number(u)
     concern = 10.0 * u

     responsibility = 7.0 + 0.40 * role - 0.70 * log(1.0 + real(bystanders)) - 0.25 * ambiguity - 0.20 * evaluation
     responsibility = max(0.0, min(10.0, responsibility))

     p = 1.0 / (1.0 + exp(-(-3.5 + 0.50 * responsibility + 0.25 * role + 0.25 * efficacy + 0.25 * concern - 0.20 * ambiguity - 0.20 * evaluation)))
     call random_number(u)
     if (u < p) interventions = interventions + 1

     responsibility_sum = responsibility_sum + responsibility
     probability_sum = probability_sum + p
  end do

  print *, "Intervention propensity model"
  print *, "Trials: ", n
  print *, "Mean perceived responsibility: ", responsibility_sum / n
  print *, "Mean intervention probability: ", probability_sum / n
  print *, "Observed intervention rate: ", real(interventions) / real(n)
end program intervention_propensity_model
