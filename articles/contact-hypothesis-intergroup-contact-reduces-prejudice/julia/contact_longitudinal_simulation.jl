#!/usr/bin/env julia

using Random
using Statistics
using Printf
using DelimitedFiles

function run_simulation(; n=5000, waves=5, seed=42, output_path="../outputs/julia_contact_longitudinal.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n * waves, 9)
    row = 1

    for i in 1:n
        prejudice = clamp(6.0 + randn(rng), 0.0, 10.0)
        anxiety = clamp(6.0 + randn(rng), 0.0, 10.0)
        empathy = clamp(4.0 + randn(rng), 0.0, 10.0)

        for wave in 1:waves
            contact_quality = clamp(5.0 + 2.0 * randn(rng), 0.0, 10.0)
            negative_contact = clamp(2.0 + 1.5 * randn(rng), 0.0, 10.0)
            institutional_support = clamp(5.0 + 2.0 * randn(rng), 0.0, 10.0)

            anxiety = clamp(anxiety - 0.18 * contact_quality + 0.28 * negative_contact - 0.05 * institutional_support + 0.25 * randn(rng), 0.0, 10.0)
            empathy = clamp(empathy + 0.16 * contact_quality - 0.12 * negative_contact + 0.20 * randn(rng), 0.0, 10.0)
            prejudice = clamp(prejudice - 0.14 * contact_quality + 0.20 * negative_contact + 0.12 * anxiety - 0.10 * empathy + 0.25 * randn(rng), 0.0, 10.0)

            rows[row, :] = [i, wave, contact_quality, negative_contact, institutional_support, anxiety, empathy, prejudice, 10.0 - prejudice]
            row += 1
        end
    end

    header = ["participant" "wave" "contact_quality" "negative_contact" "institutional_support" "intergroup_anxiety" "empathy" "prejudice" "future_contact_willingness"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Longitudinal contact simulation complete: %d participants, %d waves\n", n, waves)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
