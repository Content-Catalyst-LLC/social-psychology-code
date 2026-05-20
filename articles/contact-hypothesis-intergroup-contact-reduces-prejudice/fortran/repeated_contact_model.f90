program repeated_contact_model
  implicit none

  integer, parameter :: n = 1000
  integer :: i, wave
  real :: prejudice, anxiety, empathy, quality, negative_contact
  real :: pre_sum, post_sum
  real :: u1, u2

  call random_seed()
  pre_sum = 0.0
  post_sum = 0.0

  do i = 1, n
     call random_number(u1)
     prejudice = 4.0 + 5.0 * u1
     pre_sum = pre_sum + prejudice
     anxiety = 6.0
     empathy = 4.0

     do wave = 1, 5
        call random_number(u1)
        call random_number(u2)
        quality = 10.0 * u1
        negative_contact = 4.0 * u2

        anxiety = max(0.0, min(10.0, anxiety - 0.18 * quality + 0.28 * negative_contact))
        empathy = max(0.0, min(10.0, empathy + 0.16 * quality - 0.12 * negative_contact))
        prejudice = max(0.0, min(10.0, prejudice - 0.14 * quality + 0.20 * negative_contact + 0.12 * anxiety - 0.10 * empathy))
     end do

     post_sum = post_sum + prejudice
  end do

  print *, "Repeated contact attitude-change model"
  print *, "Participants: ", n
  print *, "Mean pre-contact prejudice: ", pre_sum / n
  print *, "Mean post-contact prejudice: ", post_sum / n
  print *, "Mean change: ", (post_sum - pre_sum) / n
end program repeated_contact_model
