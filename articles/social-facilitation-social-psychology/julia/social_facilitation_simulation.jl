#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; cases=10000, seed=42, output_path="../outputs/julia_social_facilitation_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    conditions = ["alone", "mere_presence", "evaluation", "digital_monitoring"]

    for condition in conditions
        for i in 1:cases
            baseline_skill = 10 * rand(rng)
            task_difficulty = 10 * rand(rng)
            task_mastery = clamp(baseline_skill + randn(rng) * 1.2 - 0.25 * task_difficulty, 0.0, 10.0)
            dominant_correct = task_mastery >= task_difficulty ? 1 : 0
            social_presence = condition == "alone" ? 0.0 : condition == "evaluation" ? 1.4 : condition == "digital_monitoring" ? 1.1 : 1.0
            evaluation_pressure = condition == "alone" ? 0.3 : condition == "mere_presence" ? 2.0 : condition == "evaluation" ? 8.0 : 7.0
            arousal = clamp(2.0 + 0.8 * social_presence + 0.55 * evaluation_pressure + randn(rng) * 0.9, 0.0, 10.0)
            performance = clamp(
                55 + 3.0 * baseline_skill + 2.0 * task_mastery - 2.0 * task_difficulty +
                2.0 * arousal * dominant_correct - 2.2 * arousal * (1 - dominant_correct) + randn(rng) * 5,
                0.0, 100.0
            )
            push!(rows, [condition, baseline_skill, task_difficulty, task_mastery, dominant_correct, social_presence, evaluation_pressure, arousal, performance])
        end
    end

    header = ["condition" "baseline_skill" "task_difficulty" "task_mastery" "dominant_response_correct" "social_presence" "evaluation_pressure" "arousal" "performance"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Social facilitation simulation complete. Output: %s\n", output_path)
end

run_simulation()
