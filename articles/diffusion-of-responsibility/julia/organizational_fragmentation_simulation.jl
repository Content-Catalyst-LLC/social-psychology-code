#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; n=300, periods=36, seed=42, output_path="../outputs/julia_organizational_fragmentation.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n * periods, 9)
    row = 1

    inaction_norm = 0.5 .+ 1.5 .* rand(rng, n)
    accountability = 2.0 .+ 6.0 .* rand(rng, n)
    leadership = 1.0 .+ 7.0 .* rand(rng, n)
    fragmentation = 2.0 .+ 7.0 .* rand(rng, n)
    ambiguity = 2.0 .+ 6.0 .* rand(rng, n)

    for t in 1:periods
        for i in 1:n
            responsibility = clamp(
                7.0 + 0.45 * accountability[i] + 0.30 * leadership[i] -
                0.45 * fragmentation[i] - 0.32 * ambiguity[i] -
                0.25 * inaction_norm[i] + randn(rng) * 0.65,
                0.0, 10.0
            )

            intervention_rate = logistic(
                -2.8 + 0.55 * responsibility + 0.28 * leadership[i] -
                0.30 * fragmentation[i] - 0.25 * ambiguity[i]
            )

            inaction_norm[i] = clamp(
                inaction_norm[i] + 0.22 * fragmentation[i] + 0.18 * ambiguity[i] -
                0.26 * accountability[i] - 0.22 * leadership[i] + randn(rng) * 0.35,
                0.0, 10.0
            )

            rows[row, :] = [i, t, fragmentation[i], ambiguity[i], accountability[i], leadership[i], responsibility, intervention_rate, inaction_norm[i]]
            row += 1
        end
    end

    header = ["organization_id" "period" "fragmentation" "ambiguity" "accountability_clarity" "leadership_signal" "perceived_responsibility" "intervention_rate" "inaction_norm"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Organizational fragmentation simulation complete: %d organizations, %d periods\n", n, periods)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
