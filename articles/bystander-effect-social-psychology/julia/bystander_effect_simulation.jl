#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; cases=10000, seed=42, output_path="../outputs/julia_bystander_threshold_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    conditions = ["alone", "large_group", "direct_assignment", "shared_identity", "trained_bystander", "online_harassment"]

    for condition in conditions
        for i in 1:cases
            bystanders = condition == "alone" ? 0 :
                         condition == "online_harassment" ? 30 :
                         condition == "trained_bystander" ? 30 :
                         condition == "large_group" ? 12 : 10

            direct_assignment = (condition == "direct_assignment" || condition == "trained_bystander") ? 1 : 0
            shared_identity = condition == "shared_identity" ? 8.0 : condition == "trained_bystander" ? 6.0 : 4.0
            competence = condition == "trained_bystander" ? 8.5 : 6.0
            emergency_clarity = condition == "online_harassment" ? 6.2 : condition == "direct_assignment" ? 8.5 : 7.5
            eval_app = condition == "online_harassment" ? 6.2 : 3.0

            diffusion = clamp(1 + 1.25 * log(1 + bystanders) - 2.5 * direct_assignment - 0.4 * shared_identity, 0.0, 10.0)
            responsibility = clamp(8.5 - 0.80 * diffusion + 1.8 * direct_assignment + 0.35 * shared_identity, 0.0, 10.0)
            prob = logistic(-4.0 + 0.55 * responsibility + 0.35 * emergency_clarity + 0.30 * competence - 0.35 * eval_app - 0.40 * diffusion)
            intervention = rand(rng) < prob ? 1 : 0

            push!(rows, [condition, bystanders, direct_assignment, shared_identity, competence, emergency_clarity, eval_app, diffusion, responsibility, prob, intervention])
        end
    end

    header = ["condition" "perceived_bystanders" "direct_assignment" "shared_identity" "perceived_competence" "emergency_clarity" "evaluation_apprehension" "diffusion_responsibility" "felt_responsibility" "intervention_probability" "actual_intervention"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Bystander threshold simulation complete. Output: %s\n", output_path)
end

run_simulation()
