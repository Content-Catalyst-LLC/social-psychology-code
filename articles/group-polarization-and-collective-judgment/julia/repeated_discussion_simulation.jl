#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; groups=1000, periods=18, seed=42, output_path="../outputs/julia_repeated_discussion_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    scenarios = ["homogeneous_discussion", "algorithmic_reinforcement", "cross_cutting_exposure", "structured_deliberation", "dissent_protected"]

    for scenario in scenarios
        for group in 1:groups
            attitude = (rand(rng) < 0.5 ? -1.0 : 1.0) * abs(25.0 + randn(rng) * 12.0)
            confidence = clamp(60.0 + randn(rng) * 10.0, 0.0, 100.0)

            if scenario == "homogeneous_discussion"
                homogeneity, identity, enforcement, safeguards, crosscut = 8.0, 6.5, 6.0, 3.0, 2.0
            elseif scenario == "algorithmic_reinforcement"
                homogeneity, identity, enforcement, safeguards, crosscut = 9.5, 8.0, 7.5, 2.0, 1.0
            elseif scenario == "cross_cutting_exposure"
                homogeneity, identity, enforcement, safeguards, crosscut = 3.0, 4.5, 3.0, 7.5, 9.0
            elseif scenario == "structured_deliberation"
                homogeneity, identity, enforcement, safeguards, crosscut = 3.5, 4.0, 2.5, 9.0, 8.0
            else
                homogeneity, identity, enforcement, safeguards, crosscut = 4.5, 5.0, 3.5, 8.2, 6.5
            end

            for period in 1:periods
                direction = attitude >= 0 ? 1.0 : -1.0
                amplification = 0.60*homogeneity + 0.45*identity + 0.50*enforcement - 0.65*safeguards - 0.55*crosscut + randn(rng)*2.0
                attitude = clamp(attitude + direction * amplification, -100.0, 100.0)
                confidence = clamp(confidence + 0.8*homogeneity + 0.6*enforcement - 0.7*safeguards + randn(rng)*3.0, 0.0, 100.0)
                quality = clamp(80.0 + 3.0*safeguards + 2.0*crosscut - 2.5*homogeneity - 2.0*enforcement - 0.20*abs(attitude) + randn(rng)*5.0, 0.0, 100.0)

                push!(rows, [scenario, group, period, attitude, abs(attitude), confidence, quality, homogeneity, identity, enforcement, safeguards, crosscut])
            end
        end
    end

    header = ["scenario" "group" "period" "mean_attitude" "mean_extremity" "mean_confidence" "decision_quality" "informational_homogeneity" "identity_salience" "norm_enforcement" "deliberative_safeguards" "cross_cutting_exposure"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Repeated discussion simulation complete. Output: %s\n", output_path)
end

run_simulation()
