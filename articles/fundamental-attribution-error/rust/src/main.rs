use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    disposition_sum: f64,
    situation_sum: f64,
    constraint_neglect_sum: f64,
    correspondence_sum: f64,
    blame_sum: f64,
    punishment_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/fundamental_attribution_error_trials.csv");
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
    let valence_i = idx("behavior_valence");
    let disposition_i = idx("dispositional_attribution");
    let situation_i = idx("situational_attribution");
    let actual_constraint_i = idx("actual_constraint");
    let perceived_constraint_i = idx("perceived_constraint");
    let correspondence_i = idx("correspondence_inference");
    let blame_i = idx("moral_blame");
    let punishment_i = idx("punishment_recommendation");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[valence_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        let disposition = parse_f64(fields[disposition_i]);
        let situation = parse_f64(fields[situation_i]);
        let actual = parse_f64(fields[actual_constraint_i]);
        let perceived = parse_f64(fields[perceived_constraint_i]);
        entry.disposition_sum += disposition;
        entry.situation_sum += situation;
        entry.constraint_neglect_sum += actual - perceived;
        entry.correspondence_sum += parse_f64(fields[correspondence_i]);
        entry.blame_sum += parse_f64(fields[blame_i]);
        entry.punishment_sum += parse_f64(fields[punishment_i]);
    }

    println!("ConditionValence,Trials,MeanDisposition,MeanSituation,MeanFAE,MeanConstraintNeglect,MeanCorrespondence,MeanBlame,MeanPunishment");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        let mean_disposition = s.disposition_sum / n;
        let mean_situation = s.situation_sum / n;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            mean_disposition,
            mean_situation,
            mean_disposition - mean_situation,
            s.constraint_neglect_sum / n,
            s.correspondence_sum / n,
            s.blame_sum / n,
            s.punishment_sum / n
        );
    }
}
