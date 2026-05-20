use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    performance_sum: f64,
    accuracy_sum: f64,
    error_sum: f64,
    arousal_sum: f64,
    evaluation_sum: f64,
    response_time_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/social_facilitation_trials.csv");
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
    let domain_i = idx("task_domain");
    let performance_i = idx("performance_score");
    let accuracy_i = idx("accuracy");
    let error_i = idx("error_rate");
    let arousal_i = idx("arousal_index");
    let evaluation_i = idx("evaluation_pressure");
    let response_i = idx("response_time_ms");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[domain_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.performance_sum += parse_f64(fields[performance_i]);
        entry.accuracy_sum += parse_f64(fields[accuracy_i]);
        entry.error_sum += parse_f64(fields[error_i]);
        entry.arousal_sum += parse_f64(fields[arousal_i]);
        entry.evaluation_sum += parse_f64(fields[evaluation_i]);
        entry.response_time_sum += parse_f64(fields[response_i]);
    }

    println!("ConditionDomain,Trials,MeanPerformance,MeanAccuracy,MeanErrorRate,MeanArousal,MeanEvaluation,MeanResponseTime");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.performance_sum / n,
            s.accuracy_sum / n,
            s.error_sum / n,
            s.arousal_sum / n,
            s.evaluation_sum / n,
            s.response_time_sum / n
        );
    }
}
