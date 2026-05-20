program repeated_attribution_model
  implicit none

  integer, parameter :: n = 1000
  integer, parameter :: trials = 12
  integer :: i, t, success
  real :: ego_threat, accountability, evidence
  real :: internal_attr, external_attr
  real :: int_success, int_failure, ext_success, ext_failure
  integer :: success_n, failure_n
  real :: u1, u2, u3, u4

  call random_seed()
  int_success = 0.0
  int_failure = 0.0
  ext_success = 0.0
  ext_failure = 0.0
  success_n = 0
  failure_n = 0

  do i = 1, n
     do t = 1, trials
        call random_number(u1)
        call random_number(u2)
        call random_number(u3)
        call random_number(u4)

        success = merge(1, 0, u1 < 0.5)
        ego_threat = 10.0 * u2
        accountability = 10.0 * u3
        evidence = 10.0 * u4

        internal_attr = 5.0 + 1.5 * success - 1.2 * (1 - success) + &
             0.25 * ego_threat * (2 * success - 1) - 0.20 * accountability + 0.15 * evidence
        external_attr = 5.0 - 1.0 * success + 1.5 * (1 - success) + &
             0.25 * ego_threat * (1 - success) - 0.25 * accountability + 0.10 * evidence

        internal_attr = max(0.0, min(10.0, internal_attr))
        external_attr = max(0.0, min(10.0, external_attr))

        if (success == 1) then
           int_success = int_success + internal_attr
           ext_success = ext_success + external_attr
           success_n = success_n + 1
        else
           int_failure = int_failure + internal_attr
           ext_failure = ext_failure + external_attr
           failure_n = failure_n + 1
        end if
     end do
  end do

  print *, "Repeated attribution model"
  print *, "Mean internal success: ", int_success / success_n
  print *, "Mean internal failure: ", int_failure / failure_n
  print *, "Mean external success: ", ext_success / success_n
  print *, "Mean external failure: ", ext_failure / failure_n
  print *, "Full SSB score: ", (int_success / success_n - int_failure / failure_n) + &
       (ext_failure / failure_n - ext_success / success_n)
end program repeated_attribution_model
