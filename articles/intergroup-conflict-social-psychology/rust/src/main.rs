use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    hostility_sum: f64,
    aggression_sum: f64,
    exclusion_sum: f64,
    cooperation_sum: f64,
    contact_sum: f64,
    legitimacy_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/intergroup_conflict_trials.csv");
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
    let context_i = idx("context_type");
    let hostility_i = idx("hostility_score");
    let aggression_i = idx("aggression_intention");
    let exclusion_i = idx("support_for_exclusion");
    let cooperation_i = idx("support_for_cooperation");
    let contact_i = idx("contact_quality");
    let legitimacy_i = idx("perceived_legitimacy");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.hostility_sum += parse_f64(fields[hostility_i]);
        entry.aggression_sum += parse_f64(fields[aggression_i]);
        entry.exclusion_sum += parse_f64(fields[exclusion_i]);
        entry.cooperation_sum += parse_f64(fields[cooperation_i]);
        entry.contact_sum += parse_f64(fields[contact_i]);
        entry.legitimacy_sum += parse_f64(fields[legitimacy_i]);
    }

    println!("ConditionContext,Trials,MeanHostility,MeanAggression,MeanExclusion,MeanCooperation,MeanContact,MeanLegitimacy");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.hostility_sum / n,
            s.aggression_sum / n,
            s.exclusion_sum / n,
            s.cooperation_sum / n,
            s.contact_sum / n,
            s.legitimacy_sum / n
        );
    }
}
