use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    helping_sum: f64,
    donation_sum: f64,
    cooperation_sum: f64,
    empathy_sum: f64,
    norm_sum: f64,
    efficacy_sum: f64,
    legitimacy_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/prosocial_behavior_trials.csv");
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
    let helping_i = idx("helping_decision");
    let donation_i = idx("donation_amount");
    let cooperation_i = idx("cooperation_contribution");
    let empathy_i = idx("empathy_score");
    let norm_i = idx("norm_salience");
    let efficacy_i = idx("efficacy_belief");
    let legitimacy_i = idx("institutional_legitimacy");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.helping_sum += parse_f64(fields[helping_i]);
        entry.donation_sum += parse_f64(fields[donation_i]);
        entry.cooperation_sum += parse_f64(fields[cooperation_i]);
        entry.empathy_sum += parse_f64(fields[empathy_i]);
        entry.norm_sum += parse_f64(fields[norm_i]);
        entry.efficacy_sum += parse_f64(fields[efficacy_i]);
        entry.legitimacy_sum += parse_f64(fields[legitimacy_i]);
    }

    println!("ConditionContext,Trials,HelpingRate,MeanDonation,MeanCooperation,MeanEmpathy,MeanNorms,MeanEfficacy,MeanLegitimacy");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.helping_sum / n,
            s.donation_sum / n,
            s.cooperation_sum / n,
            s.empathy_sum / n,
            s.norm_sum / n,
            s.efficacy_sum / n,
            s.legitimacy_sum / n
        );
    }
}
