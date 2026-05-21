use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    cohesion_sum: f64,
    self_censorship_sum: f64,
    dissent_sum: f64,
    quality_sum: f64,
    risk_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/groupthink_trials.csv");
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
    let context_i = idx("institution_context");
    let cohesion_i = idx("cohesion");
    let lead_i = idx("leadership_directive");
    let ins_i = idx("group_insulation");
    let stress_i = idx("stress_level");
    let consensus_i = idx("consensus_pressure");
    let self_i = idx("self_censorship");
    let dissent_i = idx("dissent_visibility");
    let outside_i = idx("outside_information");
    let quality_i = idx("decision_quality");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);

        let cohesion = parse_f64(fields[cohesion_i]);
        let lead = parse_f64(fields[lead_i]);
        let ins = parse_f64(fields[ins_i]);
        let stress = parse_f64(fields[stress_i]);
        let consensus = parse_f64(fields[consensus_i]);
        let selfc = parse_f64(fields[self_i]);
        let dissent = parse_f64(fields[dissent_i]);
        let outside = parse_f64(fields[outside_i]);
        let risk = (cohesion + lead + ins + stress + consensus + selfc - dissent - outside) / 4.0;

        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.cohesion_sum += cohesion;
        entry.self_censorship_sum += selfc;
        entry.dissent_sum += dissent;
        entry.quality_sum += parse_f64(fields[quality_i]);
        entry.risk_sum += risk;
    }

    println!("ConditionContext,Trials,MeanCohesion,MeanSelfCensorship,MeanDissent,MeanDecisionQuality,MeanRisk");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.cohesion_sum / n,
            s.self_censorship_sum / n,
            s.dissent_sum / n,
            s.quality_sum / n,
            s.risk_sum / n
        );
    }
}
