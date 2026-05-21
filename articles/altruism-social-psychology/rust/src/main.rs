use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    altruism_sum: f64,
    donation_sum: f64,
    public_goods_sum: f64,
    empathy_sum: f64,
    cost_sum: f64,
    efficacy_sum: f64,
    moral_identity_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/altruism_trials.csv");
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
    let altruism_i = idx("altruistic_decision");
    let donation_i = idx("donation_amount");
    let public_goods_i = idx("public_goods_contribution");
    let empathy_i = idx("empathy_score");
    let cost_i = idx("helping_cost");
    let efficacy_i = idx("perceived_efficacy");
    let moral_i = idx("moral_identity");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.altruism_sum += parse_f64(fields[altruism_i]);
        entry.donation_sum += parse_f64(fields[donation_i]);
        entry.public_goods_sum += parse_f64(fields[public_goods_i]);
        entry.empathy_sum += parse_f64(fields[empathy_i]);
        entry.cost_sum += parse_f64(fields[cost_i]);
        entry.efficacy_sum += parse_f64(fields[efficacy_i]);
        entry.moral_identity_sum += parse_f64(fields[moral_i]);
    }

    println!("ConditionContext,Trials,AltruismRate,MeanDonation,MeanPublicGoods,MeanEmpathy,MeanCost,MeanEfficacy,MeanMoralIdentity");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.altruism_sum / n,
            s.donation_sum / n,
            s.public_goods_sum / n,
            s.empathy_sum / n,
            s.cost_sum / n,
            s.efficacy_sum / n,
            s.moral_identity_sum / n
        );
    }
}
