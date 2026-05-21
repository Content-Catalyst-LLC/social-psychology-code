use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    intervention_sum: f64,
    likelihood_sum: f64,
    latency_sum: f64,
    bystander_sum: f64,
    responsibility_sum: f64,
    diffusion_sum: f64,
    clarity_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/bystander_effect_trials.csv");
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
    let intervention_i = idx("actual_intervention");
    let likelihood_i = idx("intervention_likelihood");
    let latency_i = idx("intervention_latency_ms");
    let bystander_i = idx("perceived_bystander_count");
    let responsibility_i = idx("felt_responsibility");
    let diffusion_i = idx("diffusion_responsibility");
    let clarity_i = idx("emergency_clarity");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.intervention_sum += parse_f64(fields[intervention_i]);
        entry.likelihood_sum += parse_f64(fields[likelihood_i]);
        entry.latency_sum += parse_f64(fields[latency_i]);
        entry.bystander_sum += parse_f64(fields[bystander_i]);
        entry.responsibility_sum += parse_f64(fields[responsibility_i]);
        entry.diffusion_sum += parse_f64(fields[diffusion_i]);
        entry.clarity_sum += parse_f64(fields[clarity_i]);
    }

    println!("ConditionContext,Trials,InterventionRate,MeanLikelihood,MeanLatency,MeanBystanders,MeanResponsibility,MeanDiffusion,MeanClarity");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.intervention_sum / n,
            s.likelihood_sum / n,
            s.latency_sum / n,
            s.bystander_sum / n,
            s.responsibility_sum / n,
            s.diffusion_sum / n,
            s.clarity_sum / n
        );
    }
}
