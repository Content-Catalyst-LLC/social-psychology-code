use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    conformed_sum: f64,
    dissented_sum: f64,
    normative_sum: f64,
    informational_sum: f64,
    confidence_shift_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/conformity_trials.csv");
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
    let context_i = idx("context");
    let conformed_i = idx("conformed");
    let dissented_i = idx("dissented");
    let normative_i = idx("normative_pressure");
    let unanimity_i = idx("unanimity");
    let cohesion_i = idx("cohesion");
    let status_i = idx("status_strength");
    let public_i = idx("public_response");
    let groupid_i = idx("group_identification");
    let dissent_i = idx("visible_dissent");
    let ambiguity_i = idx("ambiguity");
    let info_i = idx("informational_uncertainty");
    let proof_i = idx("social_proof_metrics");
    let confpre_i = idx("confidence_pre");
    let confpost_i = idx("confidence_post");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);

        let normative = (
            parse_f64(fields[normative_i])
            + parse_f64(fields[unanimity_i])
            + parse_f64(fields[cohesion_i])
            + parse_f64(fields[status_i])
            + parse_f64(fields[public_i]) * 10.0
            + parse_f64(fields[groupid_i])
            - parse_f64(fields[dissent_i])
        ) / 6.0;

        let informational = (
            parse_f64(fields[ambiguity_i])
            + parse_f64(fields[info_i])
            + parse_f64(fields[status_i])
            + parse_f64(fields[proof_i])
            - parse_f64(fields[dissent_i])
        ) / 4.0;

        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.conformed_sum += parse_f64(fields[conformed_i]);
        entry.dissented_sum += parse_f64(fields[dissented_i]);
        entry.normative_sum += normative;
        entry.informational_sum += informational;
        entry.confidence_shift_sum += parse_f64(fields[confpost_i]) - parse_f64(fields[confpre_i]);
    }

    println!("ConditionContext,Trials,ConformityRate,DissentRate,MeanNormativeInfluence,MeanInformationalInfluence,MeanConfidenceShift");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.conformed_sum / n,
            s.dissented_sum / n,
            s.normative_sum / n,
            s.informational_sum / n,
            s.confidence_shift_sum / n
        );
    }
}
