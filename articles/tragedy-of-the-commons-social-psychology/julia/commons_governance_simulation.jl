#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; groups=300, periods=60, seed=42, output_path="../outputs/julia_commons_governance_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    regimes = ["open_access", "common_property", "state_property", "polycentric"]

    resource = 80 .+ 50 .* rand(rng, groups)
    capacity = 130 .+ 50 .* rand(rng, groups)
    regen_rate = 0.08 .+ 0.08 .* rand(rng, groups)

    regime_idx = rand(rng, 1:length(regimes), groups)

    legitimacy = zeros(groups)
    monitoring = zeros(groups)
    stewardship = zeros(groups)

    for i in 1:groups
        if regimes[regime_idx[i]] == "open_access"
            legitimacy[i] = 1 + 3 * rand(rng)
            monitoring[i] = 0 + 3 * rand(rng)
            stewardship[i] = 1 + 3 * rand(rng)
        else
            legitimacy[i] = 4 + 5 * rand(rng)
            monitoring[i] = 3 + 6 * rand(rng)
            stewardship[i] = 4 + 5 * rand(rng)
        end
    end

    for t in 1:periods
        for i in 1:groups
            extraction = clamp(
                9.0 - 0.28 * legitimacy[i] - 0.25 * monitoring[i] - 0.30 * stewardship[i] + randn(rng),
                0.0, 14.0
            )
            total_extraction = 6.0 * extraction
            regeneration = max(0.0, regen_rate[i] * resource[i] * (1 - resource[i] / capacity[i]))
            resource[i] = clamp(resource[i] + regeneration - total_extraction, 0.0, capacity[i])
            depletion_risk = clamp(1 - resource[i] / capacity[i], 0.0, 1.0)

            push!(rows, [i, t, regimes[regime_idx[i]], resource[i], extraction, regeneration, legitimacy[i], monitoring[i], stewardship[i], depletion_risk])
        end
    end

    header = ["group_id" "period" "property_regime" "resource_stock" "mean_extraction" "regeneration" "legitimacy" "monitoring" "stewardship" "depletion_risk"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Commons governance simulation complete. Output: %s\n", output_path)
end

run_simulation()
