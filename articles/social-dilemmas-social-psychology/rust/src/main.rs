use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    contribution_sum: f64,
    extraction_sum: f64,
    trust_sum: f64,
    norm_sum: f64,
    legitimacy_sum: f64,
    welfare_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/social_dilemmas_trials.csv");
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
    let type_i = idx("dilemma_type");
    let contribution_i = idx("contribution");
    let extraction_i = idx("extraction");
    let trust_i = idx("trust_score");
    let norm_i = idx("norm_salience");
    let legitimacy_i = idx("institutional_legitimacy");
    let welfare_i = idx("group_welfare");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[type_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.contribution_sum += parse_f64(fields[contribution_i]);
        entry.extraction_sum += parse_f64(fields[extraction_i]);
        entry.trust_sum += parse_f64(fields[trust_i]);
        entry.norm_sum += parse_f64(fields[norm_i]);
        entry.legitimacy_sum += parse_f64(fields[legitimacy_i]);
        entry.welfare_sum += parse_f64(fields[welfare_i]);
    }

    println!("ConditionType,Trials,MeanContribution,MeanExtraction,MeanTrust,MeanNormSalience,MeanLegitimacy,MeanGroupWelfare");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.contribution_sum / n,
            s.extraction_sum / n,
            s.trust_sum / n,
            s.norm_sum / n,
            s.legitimacy_sum / n,
            s.welfare_sum / n
        );
    }
}
