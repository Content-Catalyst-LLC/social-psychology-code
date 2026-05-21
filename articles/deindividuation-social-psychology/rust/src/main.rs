use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    behavior_sum: f64,
    prosocial_sum: f64,
    antisocial_sum: f64,
    anonymity_sum: f64,
    self_awareness_sum: f64,
    accountability_sum: f64,
    norm_congruence_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/deindividuation_trials.csv");
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
    let behavior_i = idx("behavior_score");
    let prosocial_i = idx("prosocial_behavior");
    let antisocial_i = idx("antisocial_behavior");
    let anonymity_i = idx("anonymity");
    let self_awareness_i = idx("self_awareness");
    let accountability_i = idx("accountability");
    let norm_i = idx("norm_congruence");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.behavior_sum += parse_f64(fields[behavior_i]);
        entry.prosocial_sum += parse_f64(fields[prosocial_i]);
        entry.antisocial_sum += parse_f64(fields[antisocial_i]);
        entry.anonymity_sum += parse_f64(fields[anonymity_i]);
        entry.self_awareness_sum += parse_f64(fields[self_awareness_i]);
        entry.accountability_sum += parse_f64(fields[accountability_i]);
        entry.norm_congruence_sum += parse_f64(fields[norm_i]);
    }

    println!("ConditionContext,Trials,MeanBehavior,MeanProsocial,MeanAntisocial,MeanAnonymity,MeanSelfAwareness,MeanAccountability,MeanNormCongruence");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.behavior_sum / n,
            s.prosocial_sum / n,
            s.antisocial_sum / n,
            s.anonymity_sum / n,
            s.self_awareness_sum / n,
            s.accountability_sum / n,
            s.norm_congruence_sum / n
        );
    }
}
