use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    trust_sum: f64,
    fairness_sum: f64,
    empathy_sum: f64,
    blame_sum: f64,
    forgiveness_sum: f64,
    punishment_sum: f64,
    reward_sum: f64,
    resource_sum: f64,
    cooperation_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/ingroup_bias_trials.csv");
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
    let relation_i = idx("target_group_relation");
    let trust_i = idx("trust_rating");
    let fairness_i = idx("fairness_rating");
    let empathy_i = idx("empathy_rating");
    let blame_i = idx("moral_blame");
    let forgiveness_i = idx("moral_forgiveness");
    let punishment_i = idx("punishment_severity");
    let reward_i = idx("reward_allocation");
    let resource_i = idx("resource_allocation");
    let cooperation_i = idx("cooperation_choice");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[relation_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.trust_sum += parse_f64(fields[trust_i]);
        entry.fairness_sum += parse_f64(fields[fairness_i]);
        entry.empathy_sum += parse_f64(fields[empathy_i]);
        entry.blame_sum += parse_f64(fields[blame_i]);
        entry.forgiveness_sum += parse_f64(fields[forgiveness_i]);
        entry.punishment_sum += parse_f64(fields[punishment_i]);
        entry.reward_sum += parse_f64(fields[reward_i]);
        entry.resource_sum += parse_f64(fields[resource_i]);
        entry.cooperation_sum += parse_f64(fields[cooperation_i]);
    }

    println!("ConditionRelation,Trials,MeanTrust,MeanFairness,MeanEmpathy,MeanBlame,MeanForgiveness,MeanPunishment,MeanReward,MeanResource,CooperationRate");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.trust_sum / n,
            s.fairness_sum / n,
            s.empathy_sum / n,
            s.blame_sum / n,
            s.forgiveness_sum / n,
            s.punishment_sum / n,
            s.reward_sum / n,
            s.resource_sum / n,
            s.cooperation_sum / n
        );
    }
}
