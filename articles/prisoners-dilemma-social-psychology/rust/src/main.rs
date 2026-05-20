use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    cooperate_sum: f64,
    payoff_sum: f64,
    trust_sum: f64,
    fairness_sum: f64,
    expected_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/prisoners_dilemma_trials.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Could not read CSV file");
    let mut lines = content.lines();
    let header_line = lines.next().expect("Missing header");
    let headers: Vec<&str> = header_line.split(',').collect();

    let idx = |name: &str| -> usize {
        headers.iter().position(|h| *h == name).unwrap_or_else(|| panic!("Missing column: {}", name))
    };

    let condition_i = idx("condition");
    let round_i = idx("round");
    let cooperate_i = idx("cooperate");
    let payoff_i = idx("own_payoff");
    let trust_i = idx("trust_score");
    let fairness_i = idx("fairness_score");
    let expected_i = idx("expected_partner_cooperation");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:round_{}", fields[condition_i], fields[round_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.cooperate_sum += parse_f64(fields[cooperate_i]);
        entry.payoff_sum += parse_f64(fields[payoff_i]);
        entry.trust_sum += parse_f64(fields[trust_i]);
        entry.fairness_sum += parse_f64(fields[fairness_i]);
        entry.expected_sum += parse_f64(fields[expected_i]);
    }

    println!("ConditionRound,Trials,CooperationRate,MeanPayoff,MeanTrust,MeanFairness,MeanExpectedPartnerCooperation");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.cooperate_sum / n,
            s.payoff_sum / n,
            s.trust_sum / n,
            s.fairness_sum / n,
            s.expected_sum / n
        );
    }
}
