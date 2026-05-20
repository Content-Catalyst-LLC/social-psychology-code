#!/usr/bin/env julia

using Random
using Statistics
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-x))
end

function run_simulation(; n=5000, seed=42, output_path="../outputs/julia_threshold_mobilization.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n, 12)
    participate_sum = 0
    intention_sum = 0.0

    for i in 1:n
        identity = 10.0 * rand(rng)
        injustice = 10.0 * rand(rng)
        outrage = clamp(0.55 * injustice + 0.25 * identity + randn(rng), 0.0, 10.0)
        efficacy = 10.0 * rand(rng)
        network = 10.0 * rand(rng)
        cost = 10.0 * rand(rng)
        risk = 10.0 * rand(rng)
        freeride = clamp(5.0 + 0.18 * cost - 0.18 * identity + randn(rng), 0.0, 10.0)
        threshold = 6.0 + 1.2 * randn(rng)

        propensity = 0.22 * identity + 0.18 * injustice + 0.20 * outrage + 0.21 * efficacy + 0.16 * network - 0.18 * cost - 0.15 * risk - 0.08 * freeride
        intention = logistic(-2.8 + propensity)
        participate = propensity >= threshold ? 1 : 0

        participate_sum += participate
        intention_sum += intention

        rows[i, :] = [i, identity, injustice, outrage, efficacy, network, cost, risk, freeride, threshold, intention, participate]
    end

    header = ["case_id" "identity_strength" "perceived_injustice" "moral_outrage" "collective_efficacy" "network_support" "participation_cost" "repression_risk" "free_rider_incentive" "threshold" "participation_intention" "action_participation"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Threshold mobilization simulation complete: %d cases\n", n)
    @printf("Participation rate: %.3f\n", participate_sum / n)
    @printf("Mean intention: %.3f\n", intention_sum / n)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
