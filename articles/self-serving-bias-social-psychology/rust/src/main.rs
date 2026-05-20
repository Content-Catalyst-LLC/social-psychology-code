use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    internal_sum: f64,
    external_sum: f64,
    responsibility_sum: f64,
    blame_sum: f64,
    credit_sum: f64,
    excuse_sum: f64,
    learning_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/self_serving_bias_trials.csv");
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
    let valence_i = idx("outcome_valence");
    let self_other_i = idx("self_other");
    let internal_i = idx("internal_attribution");
    let external_i = idx("external_attribution");
    let responsibility_i = idx("responsibility_rating");
    let blame_i = idx("blame_rating");
    let credit_i = idx("credit_claiming");
    let excuse_i = idx("excuse_making");
    let learning_i = idx("learning_intention");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}:{}", fields[condition_i], fields[valence_i], fields[self_other_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.internal_sum += parse_f64(fields[internal_i]);
        entry.external_sum += parse_f64(fields[external_i]);
        entry.responsibility_sum += parse_f64(fields[responsibility_i]);
        entry.blame_sum += parse_f64(fields[blame_i]);
        entry.credit_sum += parse_f64(fields[credit_i]);
        entry.excuse_sum += parse_f64(fields[excuse_i]);
        entry.learning_sum += parse_f64(fields[learning_i]);
    }

    println!("ConditionValenceSelfOther,Trials,MeanInternal,MeanExternal,MeanResponsibility,MeanBlame,MeanCredit,MeanExcuse,MeanLearning");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.internal_sum / n,
            s.external_sum / n,
            s.responsibility_sum / n,
            s.blame_sum / n,
            s.credit_sum / n,
            s.excuse_sum / n,
            s.learning_sum / n
        );
    }
}
