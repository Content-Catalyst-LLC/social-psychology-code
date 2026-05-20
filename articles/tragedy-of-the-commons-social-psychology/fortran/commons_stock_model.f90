program commons_stock_model
  implicit none

  integer, parameter :: periods = 60
  integer :: t
  real :: resource, capacity, regen_rate, regeneration
  real :: extraction_per_user, total_extraction, depletion_risk

  resource = 100.0
  capacity = 150.0
  regen_rate = 0.12
  extraction_per_user = 8.0

  print *, "period,resource_stock,regeneration,total_extraction,depletion_risk"

  do t = 1, periods
     regeneration = regen_rate * resource * (1.0 - resource / capacity)
     if (regeneration < 0.0) regeneration = 0.0

     total_extraction = 6.0 * extraction_per_user
     resource = resource + regeneration - total_extraction
     if (resource < 0.0) resource = 0.0
     if (resource > capacity) resource = capacity

     depletion_risk = 1.0 - resource / capacity
     print *, t, resource, regeneration, total_extraction, depletion_risk
  end do
end program commons_stock_model
