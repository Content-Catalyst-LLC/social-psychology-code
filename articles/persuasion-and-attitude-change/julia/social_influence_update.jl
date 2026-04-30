# Toy social influence update model.

attitude = 0.20
group_norm = 0.80
influence_weight = 0.35

updated_attitude = attitude + influence_weight * (group_norm - attitude)

println("Initial attitude: ", attitude)
println("Group norm: ", group_norm)
println("Updated attitude: ", updated_attitude)
