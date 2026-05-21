program norm_equilibrium_model
  implicit none

  integer, parameter :: periods = 30
  integer :: t
  real :: perceived_compliance, approval, legitimacy, compliance_rate

  perceived_compliance = 45.0
  approval = 70.0
  legitimacy = 6.5

  print *, "period,perceived_compliance,approval,legitimacy,compliance_rate"

  do t = 1, periods
     compliance_rate = 1.0 / (1.0 + exp(-(-4.0 + 0.035 * perceived_compliance + 0.035 * approval + 0.25 * legitimacy)))
     print *, t, perceived_compliance, approval, legitimacy, compliance_rate

     perceived_compliance = 0.85 * perceived_compliance + 15.0 * compliance_rate + 2.0
     if (perceived_compliance > 100.0) perceived_compliance = 100.0
  end do
end program norm_equilibrium_model
