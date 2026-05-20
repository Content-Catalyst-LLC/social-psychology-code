use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    participation_sum: f64,
    intention_sum: f64,
    identity_sum: f64,
    injustice_sum: f64,
    outrage_sum: f64,
    efficacy_sum: f64,
    network_sum: f64,
    cost_sum: f64,
    risk_sum: f64,
    digital_sum: f64,
    offline_sum: f64,
    outcome_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/collective_action_trials.csv");
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
    let participation_i = idx("action_participation");
    let intention_i = idx("participation_intention");
    let identity_i = idx("identity_strength");
    let injustice_i = idx("perceived_injustice");
    let outrage_i = idx("moral_outrage");
    let efficacy_i = idx("collective_efficacy");
    let network_i = idx("network_support");
    let cost_i = idx("participation_cost");
    let risk_i = idx("perceived_repression_risk");
    let digital_i = idx("digital_engagement");
    let offline_i = idx("offline_engagement");
    let outcome_i = idx("movement_outcome");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let condition = fields[condition_i].to_string();
        let entry = summaries.entry(condition).or_default();
        entry.n += 1;
        entry.participation_sum += parse_f64(fields[participation_i]);
        entry.intention_sum += parse_f64(fields[intention_i]);
        entry.identity_sum += parse_f64(fields[identity_i]);
        entry.injustice_sum += parse_f64(fields[injustice_i]);
        entry.outrage_sum += parse_f64(fields[outrage_i]);
        entry.efficacy_sum += parse_f64(fields[efficacy_i]);
        entry.network_sum += parse_f64(fields[network_i]);
        entry.cost_sum += parse_f64(fields[cost_i]);
        entry.risk_sum += parse_f64(fields[risk_i]);
        entry.digital_sum += parse_f64(fields[digital_i]);
        entry.offline_sum += parse_f64(fields[offline_i]);
        entry.outcome_sum += parse_f64(fields[outcome_i]);
    }

    println!("Condition,Trials,ParticipationRate,MeanIntention,MeanIdentity,MeanInjustice,MeanOutrage,MeanEfficacy,MeanNetwork,MeanCost,MeanRisk,MeanDigital,MeanOffline,MeanOutcome");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.participation_sum / n,
            s.intention_sum / n,
            s.identity_sum / n,
            s.injustice_sum / n,
            s.outrage_sum / n,
            s.efficacy_sum / n,
            s.network_sum / n,
            s.cost_sum / n,
            s.risk_sum / n,
            s.digital_sum / n,
            s.offline_sum / n,
            s.outcome_sum / n
        );
    }
}
