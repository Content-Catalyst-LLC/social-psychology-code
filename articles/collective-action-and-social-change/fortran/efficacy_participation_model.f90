program efficacy_participation_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i, participate
  real :: identity, injustice, outrage, efficacy, network, cost, risk
  real :: propensity, intention
  real :: participation_sum, intention_sum
  real :: u1, u2, u3, u4, u5, u6, u7, u8

  call random_seed()
  participation_sum = 0.0
  intention_sum = 0.0

  do i = 1, n
     call random_number(u1)
     call random_number(u2)
     call random_number(u3)
     call random_number(u4)
     call random_number(u5)
     call random_number(u6)
     call random_number(u7)
     call random_number(u8)

     identity = 10.0 * u1
     injustice = 10.0 * u2
     efficacy = 10.0 * u3
     network = 10.0 * u4
     cost = 10.0 * u5
     risk = 10.0 * u6
     outrage = max(0.0, min(10.0, 0.55 * injustice + 0.25 * identity))

     propensity = -3.0 + 0.22 * identity + 0.18 * injustice + 0.20 * outrage + &
                  0.21 * efficacy + 0.16 * network - 0.18 * cost - 0.15 * risk

     intention = logistic(propensity)
     participate = merge(1, 0, u8 < intention)

     participation_sum = participation_sum + participate
     intention_sum = intention_sum + intention
  end do

  print *, "Collective efficacy and participation model"
  print *, "Trials: ", n
  print *, "Participation rate: ", participation_sum / n
  print *, "Mean intention: ", intention_sum / n

contains

  real function logistic(x)
    real, intent(in) :: x
    logistic = 1.0 / (1.0 + exp(-x))
  end function logistic

end program efficacy_participation_model
