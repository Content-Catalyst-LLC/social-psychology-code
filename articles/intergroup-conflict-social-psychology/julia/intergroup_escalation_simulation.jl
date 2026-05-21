#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; cases=1000, periods=15, seed=42, output_path="../outputs/julia_intergroup_escalation_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    scenarios = ["competition_only", "identity_threat", "polarization", "contact_intervention", "superordinate_goal", "low_legitimacy"]

    for scenario in scenarios
        for i in 1:cases
            conflict = scenario == "competition_only" ? 55.0 :
                       scenario == "identity_threat" ? 62.0 :
                       scenario == "polarization" ? 70.0 :
                       scenario == "contact_intervention" ? 42.0 :
                       scenario == "superordinate_goal" ? 40.0 : 66.0

            threat = scenario == "identity_threat" ? 8.5 :
                     scenario == "polarization" ? 8.0 :
                     scenario == "contact_intervention" ? 4.0 :
                     scenario == "superordinate_goal" ? 4.2 : 7.0

            contact = scenario == "contact_intervention" ? 8.0 :
                      scenario == "superordinate_goal" ? 7.5 : 2.5
            common_goal = scenario == "superordinate_goal" ? 9.0 :
                          scenario == "contact_intervention" ? 6.5 : 2.5
            legitimacy = scenario == "low_legitimacy" ? 2.5 :
                         scenario == "contact_intervention" ? 7.0 :
                         scenario == "superordinate_goal" ? 7.5 : 4.5
            retaliation = scenario == "polarization" ? 8.5 :
                          scenario == "identity_threat" ? 7.0 :
                          scenario == "low_legitimacy" ? 7.0 : 5.0

            for period in 1:periods
                hostility = clamp(0.55*conflict + 3.0*threat + 2.5*retaliation - 2.8*contact - 2.5*common_goal - 2.5*legitimacy + randn(rng)*5.0, 0.0, 100.0)
                threat = clamp(threat + 0.020*hostility - 0.22*contact - 0.22*common_goal - 0.15*legitimacy + randn(rng)*0.25, 0.0, 10.0)
                conflict = clamp(conflict + 0.25*hostility + 2.5*threat + 1.5*retaliation - 3.0*contact - 3.2*common_goal - 2.0*legitimacy + randn(rng)*5.0, 0.0, 100.0)

                push!(rows, [scenario, period, conflict, threat, contact, common_goal, legitimacy, retaliation, hostility])
            end
        end
    end

    header = ["scenario" "period" "conflict_intensity" "perceived_threat" "contact_quality" "common_goal_salience" "institutional_legitimacy" "norm_of_retaliation" "hostile_interaction"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Intergroup escalation simulation complete. Output: %s\n", output_path)
end

run_simulation()
