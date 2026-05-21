program escalation_recurrence_model
  implicit none

  integer, parameter :: periods = 25
  integer :: t
  real :: conflict, threat, contact, goal, legitimacy, retaliation, hostility

  conflict = 55.0
  threat = 6.5
  contact = 2.5
  goal = 2.5
  legitimacy = 4.5
  retaliation = 6.0

  print *, "period,conflict,threat,hostility"

  do t = 1, periods
     hostility = max(0.0, min(100.0, 0.55 * conflict + 3.0 * threat + 2.5 * retaliation - 2.8 * contact - 2.5 * goal - 2.5 * legitimacy))
     threat = max(0.0, min(10.0, threat + 0.020 * hostility - 0.22 * contact - 0.22 * goal - 0.15 * legitimacy))
     conflict = max(0.0, min(100.0, conflict + 0.25 * hostility + 2.5 * threat + 1.5 * retaliation - 3.0 * contact - 3.2 * goal - 2.0 * legitimacy))
     print *, t, conflict, threat, hostility
  end do
end program escalation_recurrence_model
