use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    abs_error_sum: f64,
    calibration_sum: f64,
    overconfidence_sum: f64,
    quality_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/heuristics_biases_trials.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Could not read CSV file");
    let mut lines = content.lines();
    let header_line = lines.next().expect("Missing header");
    let headers: Vec<&str> = header_line.split(',').collect();

    let idx = |name: &str| -> usize {
        headers.iter().position(|h| *h == name).unwrap_or_else(|| panic!("Missing column: {}", name))
    };

    let heuristic_i = idx("heuristic_type");
    let condition_i = idx("condition");
    let estimate_i = idx("estimate");
    let true_i = idx("true_value");
    let confidence_i = idx("confidence_rating");
    let accuracy_i = idx("actual_accuracy");
    let overconfidence_i = idx("overconfidence_score");
    let quality_i = idx("decision_quality");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[heuristic_i], fields[condition_i]);

        let estimate = parse_f64(fields[estimate_i]);
        let true_value = parse_f64(fields[true_i]);
        let confidence = parse_f64(fields[confidence_i]);
        let accuracy = parse_f64(fields[accuracy_i]);

        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.abs_error_sum += (estimate - true_value).abs();
        entry.calibration_sum += (confidence - accuracy).abs();
        entry.overconfidence_sum += parse_f64(fields[overconfidence_i]);
        entry.quality_sum += parse_f64(fields[quality_i]);
    }

    println!("HeuristicCondition,Trials,MeanAbsError,MeanCalibrationError,MeanOverconfidence,MeanDecisionQuality");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.abs_error_sum / n,
            s.calibration_sum / n,
            s.overconfidence_sum / n,
            s.quality_sum / n
        );
    }
}
