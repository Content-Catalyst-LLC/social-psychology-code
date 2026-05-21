program escalation_recurrence
  implicit none

  integer, parameter :: steps = 12
  integer :: t
  real :: obedience, legitimacy, dissent, displacement, moral, latent, probability

  legitimacy = 8.0
  dissent = 2.0
  displacement = 7.5
  moral = 5.5
  obedience = 0.0

  print *, "step,legitimacy,peer_dissent,responsibility_displacement,moral_conflict,obedience_probability"

  do t = 1, steps
     latent = -2.1 + 0.38*legitimacy + 0.20*t + 0.32*displacement - 0.36*dissent - 0.30*moral
     probability = 1.0 / (1.0 + exp(-latent))
     obedience = probability
     print *, t, legitimacy, dissent, displacement, moral, obedience
  end do
end program escalation_recurrence
