use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    extraction_sum: f64,
    stock_sum: f64,
    trust_sum: f64,
    legitimacy_sum: f64,
    monitoring_sum: f64,
    depletion_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/tragedy_commons_trials.csv");
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
    let regime_i = idx("property_regime");
    let extraction_i = idx("extraction");
    let stock_i = idx("resource_stock");
    let trust_i = idx("trust_score");
    let legitimacy_i = idx("legitimacy_score");
    let monitoring_i = idx("monitoring_credibility");
    let depletion_i = idx("depletion_risk");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[regime_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.extraction_sum += parse_f64(fields[extraction_i]);
        entry.stock_sum += parse_f64(fields[stock_i]);
        entry.trust_sum += parse_f64(fields[trust_i]);
        entry.legitimacy_sum += parse_f64(fields[legitimacy_i]);
        entry.monitoring_sum += parse_f64(fields[monitoring_i]);
        entry.depletion_sum += parse_f64(fields[depletion_i]);
    }

    println!("ConditionRegime,Trials,MeanExtraction,MeanResourceStock,MeanTrust,MeanLegitimacy,MeanMonitoring,MeanDepletionRisk");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.extraction_sum / n,
            s.stock_sum / n,
            s.trust_sum / n,
            s.legitimacy_sum / n,
            s.monitoring_sum / n,
            s.depletion_sum / n
        );
    }
}
