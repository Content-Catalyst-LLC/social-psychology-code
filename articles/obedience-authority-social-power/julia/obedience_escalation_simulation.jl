#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

logistic(x) = 1.0 / (1.0 + exp(-x))

function run_simulation(; participants=1000, steps=12, seed=42, output_path="../outputs/julia_obedience_escalation_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    scenarios = ["high_legitimacy", "peer_dissent", "high_responsibility", "mission_identification", "low_legitimacy", "visible_harm", "resistance_support"]

    for scenario in scenarios
        for participant in 1:participants
            for step in 1:steps
                legitimacy = (scenario == "high_legitimacy" ? 8.8 : scenario == "mission_identification" ? 8.0 : scenario == "low_legitimacy" ? 3.0 : 7.0) + randn(rng)*0.8
                dissent = (scenario == "peer_dissent" ? 8.5 : scenario == "resistance_support" ? 8.2 : scenario == "visible_harm" ? 5.5 : scenario == "low_legitimacy" ? 4.5 : 1.8) + randn(rng)*0.8
                responsibility = (scenario == "high_responsibility" ? 8.8 : scenario == "visible_harm" ? 8.2 : scenario == "resistance_support" ? 8.0 : 3.5) + randn(rng)*0.8
                moral = (scenario == "visible_harm" ? 8.8 : scenario == "high_responsibility" ? 8.0 : scenario == "peer_dissent" ? 7.2 : scenario == "resistance_support" ? 7.8 : 5.2) + randn(rng)*0.8
                identification = (scenario == "mission_identification" ? 9.0 : scenario == "high_legitimacy" ? 7.2 : 4.8) + randn(rng)*0.8
                displacement = clamp(10.0 - responsibility, 0.0, 10.0)

                latent = -2.1 + 0.38*legitimacy + 0.25*identification + 0.20*step + 0.32*displacement - 0.36*dissent - 0.30*moral - 0.24*responsibility
                prob = logistic(latent)
                obeyed = rand(rng) < prob ? 1 : 0

                push!(rows, [scenario, participant, step, clamp(legitimacy,0,10), clamp(dissent,0,10), clamp(responsibility,0,10), displacement, clamp(moral,0,10), clamp(identification,0,10), prob, obeyed])
            end
        end
    end

    header = ["scenario" "participant" "escalation_step" "authority_legitimacy" "peer_dissent" "perceived_responsibility" "responsibility_displacement" "moral_conflict" "identification" "obedience_probability" "obeyed"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Obedience escalation simulation complete. Output: %s\n", output_path)
end

run_simulation()
