#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; groups=250, periods=50, seed=42, output_path="../outputs/julia_commons_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]

    resource = 70 .+ 50 .* rand(rng, groups)
    monitoring = 1 .+ 8 .* rand(rng, groups)
    legitimacy = 1 .+ 8 .* rand(rng, groups)
    sanction = 8 .* rand(rng, groups)
    norm = 1 .+ 8 .* rand(rng, groups)

    for t in 1:periods
        for g in 1:groups
            extraction = clamp(
                8.5 - 0.25 * monitoring[g] - 0.25 * legitimacy[g] -
                0.25 * sanction[g] - 0.25 * norm[g] + randn(rng),
                0.0, 15.0
            )
            total_extraction = 6.0 * extraction
            regeneration = max(0.0, 0.12 * resource[g] * (1 - resource[g] / 150.0))
            resource[g] = clamp(resource[g] + regeneration - total_extraction, 0.0, 150.0)

            push!(rows, [g, t, resource[g], extraction, monitoring[g], legitimacy[g], sanction[g], norm[g]])
        end
    end

    header = ["group_id" "period" "resource_stock" "mean_extraction" "monitoring" "legitimacy" "sanction" "norm_salience"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Commons simulation complete. Output: %s\n", output_path)
end

run_simulation()
