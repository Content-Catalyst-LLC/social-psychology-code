#!/usr/bin/env julia

using Random
using Statistics
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; n=250, periods=40, seed=42, output_path="../outputs/julia_institutional_normalization.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n * periods, 8)
    row = 1

    normalized_harm = 0.5 .+ 1.5 .* rand(rng, n)
    accountability = 2.0 .+ 6.0 .* rand(rng, n)
    dissent_protection = 2.0 .+ 6.0 .* rand(rng, n)
    reward_for_harm = 1.0 .+ 7.0 .* rand(rng, n)

    for t in 1:periods
        for i in 1:n
            md = clamp(
                2.5 + 0.35 * normalized_harm[i] + 0.35 * reward_for_harm[i] -
                0.25 * accountability[i] - 0.25 * dissent_protection[i] + randn(rng) * 0.8,
                0.0, 10.0
            )

            harmful_rate = logistic(-3.0 + 0.55 * md + 0.25 * reward_for_harm[i] - 0.28 * accountability[i])

            normalized_harm[i] = clamp(
                normalized_harm[i] + 0.18 * md + 0.22 * reward_for_harm[i] -
                0.25 * accountability[i] - 0.20 * dissent_protection[i] + randn(rng) * 0.45,
                0.0, 10.0
            )

            rows[row, :] = [i, t, md, harmful_rate, normalized_harm[i], accountability[i], dissent_protection[i], reward_for_harm[i]]
            row += 1
        end
    end

    header = ["institution_id" "period" "moral_disengagement" "harmful_rate" "normalized_harm" "accountability" "dissent_protection" "reward_for_harm"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Institutional normalization simulation complete: %d institutions, %d periods\n", n, periods)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
