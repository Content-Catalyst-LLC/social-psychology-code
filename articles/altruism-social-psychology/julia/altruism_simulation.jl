#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; cases=10000, seed=42, output_path="../outputs/julia_altruism_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    conditions = ["high_empathy", "high_cost", "anonymous_helping", "public_helping", "kin_recipient", "public_goods", "altruistic_punishment"]

    for condition in conditions
        for i in 1:cases
            empathy = condition == "high_empathy" ? 8.5 : condition == "public_helping" ? 6.2 : 7.0
            cost = condition == "high_cost" ? 8.5 : condition == "kin_recipient" ? 5.5 : 4.0
            need = 7.0
            identity = condition == "kin_recipient" ? 8.5 : condition == "public_goods" ? 5.0 : 4.0
            kin = condition == "kin_recipient" ? 0.5 : 0.0
            reputation = condition == "public_helping" ? 8.0 : condition == "anonymous_helping" ? 0.5 : 3.0
            moral = 7.0
            norms = condition == "public_goods" || condition == "altruistic_punishment" ? 8.0 : 5.5
            warm = 6.0
            efficacy = condition == "public_goods" ? 8.5 : 6.5
            risk = condition == "high_cost" ? 7.5 : condition == "altruistic_punishment" ? 4.0 : 3.0

            latent = -4.2 + 0.34*empathy + 0.20*need + 0.25*identity + 1.4*kin + 0.10*reputation + 0.28*moral + 0.20*norms + 0.18*warm + 0.30*efficacy - 0.36*cost - 0.24*risk
            prob = logistic(latent)
            decision = rand(rng) < prob ? 1 : 0
            donation = clamp(4 + 8.5*decision + 4.2*empathy + 2.2*moral + 2.0*efficacy + 1.7*warm + 1.2*reputation - 3.0*cost - 1.5*risk + randn(rng)*7.0, 0.0, 100.0)

            push!(rows, [condition, empathy, cost, need, identity, kin, reputation, moral, norms, warm, efficacy, risk, prob, decision, donation])
        end
    end

    header = ["condition" "empathy_score" "helping_cost" "recipient_need" "identity_overlap" "kinship_coefficient" "reputation_visibility" "moral_identity" "social_norm_salience" "warm_glow_expectation" "perceived_efficacy" "intervention_risk" "altruism_probability" "altruistic_decision" "donation_amount"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Altruism simulation complete. Output: %s\n", output_path)
end

run_simulation()
