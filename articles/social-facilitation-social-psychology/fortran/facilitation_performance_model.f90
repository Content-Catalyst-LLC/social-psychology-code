program facilitation_performance_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i, audience, dominant_correct
  real :: u, baseline_skill, task_difficulty, task_mastery
  real :: evaluation_pressure, arousal, performance
  real :: perf_alone, perf_audience
  integer :: n_alone, n_audience

  call random_seed()
  perf_alone = 0.0
  perf_audience = 0.0
  n_alone = 0
  n_audience = 0

  do i = 1, n
     audience = mod(i, 2)

     call random_number(u)
     baseline_skill = 10.0 * u
     call random_number(u)
     task_difficulty = 10.0 * u
     task_mastery = baseline_skill - 0.25 * task_difficulty
     if (task_mastery < 0.0) task_mastery = 0.0
     if (task_mastery > 10.0) task_mastery = 10.0

     if (task_mastery >= task_difficulty) then
        dominant_correct = 1
     else
        dominant_correct = 0
     end if

     if (audience == 1) then
        evaluation_pressure = 6.0
     else
        evaluation_pressure = 0.5
     end if

     arousal = 2.0 + 0.8 * audience + 0.55 * evaluation_pressure
     performance = 55.0 + 3.0 * baseline_skill + 2.0 * task_mastery - 2.0 * task_difficulty + &
        2.0 * arousal * dominant_correct - 2.2 * arousal * (1 - dominant_correct)

     if (performance < 0.0) performance = 0.0
     if (performance > 100.0) performance = 100.0

     if (audience == 1) then
        perf_audience = perf_audience + performance
        n_audience = n_audience + 1
     else
        perf_alone = perf_alone + performance
        n_alone = n_alone + 1
     end if
  end do

  print *, "Social facilitation performance model"
  print *, "Trials: ", n
  print *, "Mean performance alone: ", perf_alone / real(n_alone)
  print *, "Mean performance with audience: ", perf_audience / real(n_audience)
end program facilitation_performance_model
