use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    stereotype_sum: f64,
    prejudice_sum: f64,
    discrimination_sum: f64,
    contact_sum: f64,
    threat_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/stereotypes_prejudice_trials.csv");
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
    let stereotype_i = idx("stereotype_strength");
    let prejudice_i = idx("prejudice_rating");
    let discrimination_i = idx("discrimination_tendency");
    let contact_i = idx("contact_quality");
    let support_i = idx("institutional_support");
    let threat_i = idx("perceived_threat");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);

        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.stereotype_sum += parse_f64(fields[stereotype_i]);
        entry.prejudice_sum += parse_f64(fields[prejudice_i]);
        entry.discrimination_sum += parse_f64(fields[discrimination_i]);
        entry.contact_sum += (parse_f64(fields[contact_i]) + parse_f64(fields[support_i])) / 2.0;
        entry.threat_sum += parse_f64(fields[threat_i]);
    }

    println!("ConditionContext,Trials,MeanStereotype,MeanPrejudice,MeanDiscrimination,MeanContactSupport,MeanThreat");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.stereotype_sum / n,
            s.prejudice_sum / n,
            s.discrimination_sum / n,
            s.contact_sum / n,
            s.threat_sum / n
        );
    }
}
