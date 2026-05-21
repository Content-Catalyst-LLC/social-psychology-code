program repeated_discussion_recurrence
  implicit none

  integer, parameter :: periods = 25
  integer :: t
  real :: attitude, confidence, homogeneity, identity, enforcement, safeguards, crosscut, amplification, quality

  attitude = 25.0
  confidence = 60.0
  homogeneity = 8.0
  identity = 7.0
  enforcement = 7.0
  safeguards = 3.0
  crosscut = 2.0

  print *, "period,mean_attitude,mean_extremity,confidence,decision_quality"

  do t = 1, periods
     amplification = 0.60 * homogeneity + 0.45 * identity + 0.50 * enforcement - 0.65 * safeguards - 0.55 * crosscut

     if (attitude >= 0.0) then
        attitude = attitude + amplification
     else
        attitude = attitude - amplification
     end if

     if (attitude > 100.0) attitude = 100.0
     if (attitude < -100.0) attitude = -100.0

     confidence = confidence + 0.8 * homogeneity + 0.6 * enforcement - 0.7 * safeguards
     if (confidence > 100.0) confidence = 100.0
     if (confidence < 0.0) confidence = 0.0

     quality = 80.0 + 3.0 * safeguards + 2.0 * crosscut - 2.5 * homogeneity - 2.0 * enforcement - 0.20 * abs(attitude)
     if (quality > 100.0) quality = 100.0
     if (quality < 0.0) quality = 0.0

     print *, t, attitude, abs(attitude), confidence, quality
  end do
end program repeated_discussion_recurrence
