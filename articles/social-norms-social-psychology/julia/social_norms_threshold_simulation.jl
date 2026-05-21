#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; cases=10000, seed=42, output_path="../outputs/julia_norm_threshold_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    scenarios = ["stable_low_norm", "stable_high_norm", "dynamic_growth", "injunctive_boost", "boomerang_risk", "legitimacy_loss"]

    for scenario in scenarios
        for i in 1:cases
            perceived_compliance = scenario == "stable_low_norm" ? 35.0 :
                                   scenario == "stable_high_norm" ? 78.0 :
                                   scenario == "dynamic_growth" ? 46.0 :
                                   scenario == "injunctive_boost" ? 50.0 :
                                   scenario == "boomerang_risk" ? 45.0 : 70.0
            approval = scenario == "stable_low_norm" ? 42.0 :
                       scenario == "stable_high_norm" ? 84.0 :
                       scenario == "dynamic_growth" ? 62.0 :
                       scenario == "injunctive_boost" ? 88.0 :
                       scenario == "boomerang_risk" ? 35.0 : 80.0
            trend = scenario == "dynamic_growth" ? 40.0 :
                    scenario == "injunctive_boost" ? 8.0 :
                    scenario == "boomerang_risk" ? -10.0 : 2.0
            legitimacy = scenario == "legitimacy_loss" ? 2.5 :
                         scenario == "stable_high_norm" ? 7.0 : 6.0

            threshold = clamp(55.0 + randn(rng) * 12.0, 0.0, 100.0)
            tipping_exposure = clamp(perceived_compliance + 0.45 * max(0.0, trend) + 0.20 * approval + randn(rng) * 8.0, 0.0, 100.0)
            tipping_margin = tipping_exposure - threshold
            prob = logistic(-3.0 + 0.030 * perceived_compliance + 0.030 * approval + 0.020 * trend + 0.25 * legitimacy + 0.035 * tipping_margin)
            complied = rand(rng) < prob ? 1 : 0

            push!(rows, [scenario, perceived_compliance, approval, trend, legitimacy, threshold, tipping_exposure, tipping_margin, prob, complied])
        end
    end

    header = ["scenario" "perceived_compliance" "perceived_approval" "dynamic_norm_trend" "institutional_legitimacy" "norm_threshold" "tipping_exposure" "tipping_margin" "compliance_probability" "complied"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Norm threshold simulation complete. Output: %s\n", output_path)
end

run_simulation()
