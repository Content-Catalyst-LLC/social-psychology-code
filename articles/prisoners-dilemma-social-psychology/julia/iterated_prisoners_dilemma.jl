#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function payoff(a, b; T=5.0, R=3.0, P=1.0, S=0.0)
    if a == 1 && b == 1
        return R
    elseif a == 1 && b == 0
        return S
    elseif a == 0 && b == 1
        return T
    else
        return P
    end
end

function choose(strategy, own_hist, opp_hist, rng)
    if strategy == "always_cooperate"
        return 1
    elseif strategy == "always_defect"
        return 0
    elseif strategy == "tit_for_tat"
        return isempty(opp_hist) ? 1 : opp_hist[end]
    elseif strategy == "generous_tit_for_tat"
        if isempty(opp_hist)
            return 1
        elseif opp_hist[end] == 0 && rand(rng) < 0.15
            return 1
        else
            return opp_hist[end]
        end
    elseif strategy == "win_stay_lose_shift"
        if isempty(own_hist)
            return 1
        end
        last_payoff = payoff(own_hist[end], opp_hist[end])
        return last_payoff >= 3.0 ? own_hist[end] : 1 - own_hist[end]
    else
        return 0
    end
end

function run_tournament(; rounds=200, seed=42, output_path="../outputs/julia_strategy_tournament.csv")
    rng = MersenneTwister(seed)
    strategies = ["always_cooperate", "always_defect", "tit_for_tat", "generous_tit_for_tat", "win_stay_lose_shift"]
    rows = Any[]

    for s1 in strategies
        for s2 in strategies
            h1 = Int[]
            h2 = Int[]
            score1 = 0.0
            score2 = 0.0
            for r in 1:rounds
                c1 = choose(s1, h1, h2, rng)
                c2 = choose(s2, h2, h1, rng)
                p1 = payoff(c1, c2)
                p2 = payoff(c2, c1)
                score1 += p1
                score2 += p2
                push!(h1, c1)
                push!(h2, c2)
                push!(rows, [s1, s2, r, c1, c2, p1, p2, score1, score2])
            end
        end
    end

    header = ["strategy_a" "strategy_b" "round" "choice_a" "choice_b" "payoff_a" "payoff_b" "cumulative_a" "cumulative_b"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Iterated prisoner’s dilemma tournament complete. Output: %s\n", output_path)
end

run_tournament()
