program hamilton_rule_model
  implicit none

  integer :: i, j
  real :: r, benefit, cost
  logical :: selected

  print *, "relatedness,benefit,cost,hamilton_selected"

  do i = 0, 10
     r = real(i) / 10.0
     do j = 1, 10
        benefit = real(j)
        cost = 3.0
        selected = (r * benefit > cost)
        print *, r, benefit, cost, selected
     end do
  end do
end program hamilton_rule_model
