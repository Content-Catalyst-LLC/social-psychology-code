use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    compliance_sum: f64,
    intention_sum: f64,
    contribution_sum: f64,
    descriptive_sum: f64,
    injunctive_sum: f64,
    empirical_sum: f64,
    normative_sum: f64,
    legitimacy_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/social_norms_trials.csv");
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
    let domain_i = idx("policy_domain");
    let message_i = idx("message_type");
    let complied_i = idx("complied");
    let intention_i = idx("compliance_intention");
    let contribution_i = idx("contribution_amount");
    let descriptive_i = idx("descriptive_norm");
    let injunctive_i = idx("injunctive_norm");
    let empirical_i = idx("empirical_expectation");
    let normative_i = idx("normative_expectation");
    let legitimacy_i = idx("institutional_legitimacy");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}:{}", fields[condition_i], fields[domain_i], fields[message_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.compliance_sum += parse_f64(fields[complied_i]);
        entry.intention_sum += parse_f64(fields[intention_i]);
        entry.contribution_sum += parse_f64(fields[contribution_i]);
        entry.descriptive_sum += parse_f64(fields[descriptive_i]);
        entry.injunctive_sum += parse_f64(fields[injunctive_i]);
        entry.empirical_sum += parse_f64(fields[empirical_i]);
        entry.normative_sum += parse_f64(fields[normative_i]);
        entry.legitimacy_sum += parse_f64(fields[legitimacy_i]);
    }

    println!("ConditionDomainMessage,Trials,ComplianceRate,MeanIntention,MeanContribution,MeanDescriptive,MeanInjunctive,MeanEmpirical,MeanNormative,MeanLegitimacy");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.compliance_sum / n,
            s.intention_sum / n,
            s.contribution_sum / n,
            s.descriptive_sum / n,
            s.injunctive_sum / n,
            s.empirical_sum / n,
            s.normative_sum / n,
            s.legitimacy_sum / n
        );
    }
}
