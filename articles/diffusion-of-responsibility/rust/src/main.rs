use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    bystander_sum: f64,
    intervention_sum: f64,
    reporting_sum: f64,
    responsibility_sum: f64,
    role_sum: f64,
    ambiguity_sum: f64,
    delay_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/diffusion_responsibility_trials.csv");
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
    let domain_i = idx("scenario_domain");
    let bystander_i = idx("bystander_count");
    let intervention_i = idx("intervention_decision");
    let reporting_i = idx("reporting_decision");
    let responsibility_i = idx("perceived_responsibility");
    let role_i = idx("role_clarity");
    let ambiguity_i = idx("ambiguity_level");
    let delay_i = idx("intervention_delay_seconds");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[domain_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.bystander_sum += parse_f64(fields[bystander_i]);
        entry.intervention_sum += parse_f64(fields[intervention_i]);
        entry.reporting_sum += parse_f64(fields[reporting_i]);
        entry.responsibility_sum += parse_f64(fields[responsibility_i]);
        entry.role_sum += parse_f64(fields[role_i]);
        entry.ambiguity_sum += parse_f64(fields[ambiguity_i]);
        entry.delay_sum += parse_f64(fields[delay_i]);
    }

    println!("ConditionDomain,Trials,MeanBystanders,InterventionRate,ReportingRate,MeanResponsibility,MeanRoleClarity,MeanAmbiguity,MeanDelay");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.bystander_sum / n,
            s.intervention_sum / n,
            s.reporting_sum / n,
            s.responsibility_sum / n,
            s.role_sum / n,
            s.ambiguity_sum / n,
            s.delay_sum / n
        );
    }
}
