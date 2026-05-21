use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    shift_sum: f64,
    extremity_shift_sum: f64,
    confidence_shift_sum: f64,
    quality_sum: f64,
    accuracy_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/group_polarization_trials.csv");
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
    let context_i = idx("platform_context");
    let pre_i = idx("pre_attitude");
    let post_i = idx("post_attitude");
    let pre_conf_i = idx("pre_confidence");
    let post_conf_i = idx("post_confidence");
    let quality_i = idx("decision_quality");
    let accuracy_i = idx("collective_judgment_accuracy");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);
        let pre = parse_f64(fields[pre_i]);
        let post = parse_f64(fields[post_i]);
        let pre_conf = parse_f64(fields[pre_conf_i]);
        let post_conf = parse_f64(fields[post_conf_i]);

        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.shift_sum += post - pre;
        entry.extremity_shift_sum += post.abs() - pre.abs();
        entry.confidence_shift_sum += post_conf - pre_conf;
        entry.quality_sum += parse_f64(fields[quality_i]);
        entry.accuracy_sum += parse_f64(fields[accuracy_i]);
    }

    println!("ConditionContext,Trials,MeanShift,MeanExtremityShift,MeanConfidenceShift,MeanDecisionQuality,MeanAccuracy");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.shift_sum / n,
            s.extremity_shift_sum / n,
            s.confidence_shift_sum / n,
            s.quality_sum / n,
            s.accuracy_sum / n
        );
    }
}
