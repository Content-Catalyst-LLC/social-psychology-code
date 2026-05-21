program consensus_pressure_recurrence
  implicit none

  integer, parameter :: periods = 20
  integer :: t
  real :: risk, safeguards, stress, dissent, consensus, selfcens, quality, implrisk

  risk = 7.5
  safeguards = 2.5
  stress = 8.0
  dissent = 2.5
  quality = 60.0

  print *, "period,consensus_pressure,self_censorship,decision_quality,implementation_risk"

  do t = 1, periods
     consensus = max(0.0, min(10.0, risk + 0.15 * t))
     selfcens = max(0.0, min(10.0, 0.65*risk + 0.45*stress + 0.55*consensus - 0.60*safeguards - 0.45*dissent))
     quality = max(0.0, min(100.0, quality - 2.2*risk - 1.5*selfcens + 2.8*safeguards + 2.0*dissent))
     implrisk = max(0.0, min(100.0, 75.0 + 2.5*risk + 2.0*selfcens - 2.5*safeguards - 1.8*dissent))

     print *, t, consensus, selfcens, quality, implrisk
  end do
end program consensus_pressure_recurrence
