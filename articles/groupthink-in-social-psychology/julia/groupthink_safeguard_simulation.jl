#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; groups=1000, periods=12, seed=42, output_path="../outputs/julia_groupthink_safeguard_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    scenarios = ["unstructured_crisis", "directive_leader", "devils_advocate", "outside_experts", "red_team", "second_chance_meeting"]

    for scenario in scenarios
        for group in 1:groups
            if scenario == "unstructured_crisis"
                risk, safeguards, stress, dissent = 7.5, 2.5, 8.5, 2.5
            elseif scenario == "directive_leader"
                risk, safeguards, stress, dissent = 8.0, 2.0, 7.0, 2.0
            elseif scenario == "devils_advocate"
                risk, safeguards, stress, dissent = 5.0, 7.0, 6.0, 7.5
            elseif scenario == "outside_experts"
                risk, safeguards, stress, dissent = 4.5, 7.8, 6.0, 7.2
            elseif scenario == "red_team"
                risk, safeguards, stress, dissent = 4.0, 8.5, 6.5, 8.5
            else
                risk, safeguards, stress, dissent = 4.2, 8.0, 7.0, 8.0
            end

            quality = clamp(60.0 + randn(rng)*8.0, 0.0, 100.0)

            for period in 1:periods
                consensus = clamp(risk + 0.15*period + randn(rng)*0.8, 0.0, 10.0)
                selfcens = clamp(0.65*risk + 0.45*stress + 0.55*consensus - 0.60*safeguards - 0.45*dissent + randn(rng), 0.0, 10.0)
                quality = clamp(quality - 2.2*risk - 1.5*selfcens + 2.8*safeguards + 2.0*dissent + randn(rng)*5.0, 0.0, 100.0)
                implrisk = clamp(75.0 + 2.5*risk + 2.0*selfcens - 2.5*safeguards - 1.8*dissent + randn(rng)*6.0, 0.0, 100.0)

                push!(rows, [scenario, group, period, risk, safeguards, stress, dissent, consensus, selfcens, quality, implrisk])
            end
        end
    end

    header = ["scenario" "group" "period" "groupthink_risk" "safeguards" "stress" "dissent_visibility" "consensus_pressure" "self_censorship" "decision_quality" "implementation_risk"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Groupthink safeguard simulation complete. Output: %s\n", output_path)
end

run_simulation()
