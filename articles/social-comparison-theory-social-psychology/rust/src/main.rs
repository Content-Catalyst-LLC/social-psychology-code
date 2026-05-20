use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    gap_sum: f64,
    attainability_sum: f64,
    eval_change_sum: f64,
    motivation_sum: f64,
    envy_sum: f64,
    inspiration_sum: f64,
    discouragement_sum: f64,
    relative_deprivation_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/social_comparison_trials.csv");
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
    let comparison_i = idx("comparison_type");
    let gap_i = idx("comparison_gap");
    let attainability_i = idx("attainability");
    let pre_i = idx("self_eval_pre");
    let post_i = idx("self_eval_post");
    let motivation_i = idx("motivation_score");
    let envy_i = idx("envy");
    let inspiration_i = idx("inspiration");
    let discouragement_i = idx("discouragement");
    let rd_i = idx("relative_deprivation");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[comparison_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.gap_sum += parse_f64(fields[gap_i]);
        entry.attainability_sum += parse_f64(fields[attainability_i]);
        entry.eval_change_sum += parse_f64(fields[post_i]) - parse_f64(fields[pre_i]);
        entry.motivation_sum += parse_f64(fields[motivation_i]);
        entry.envy_sum += parse_f64(fields[envy_i]);
        entry.inspiration_sum += parse_f64(fields[inspiration_i]);
        entry.discouragement_sum += parse_f64(fields[discouragement_i]);
        entry.relative_deprivation_sum += parse_f64(fields[rd_i]);
    }

    println!("ConditionComparison,Trials,MeanGap,MeanAttainability,MeanSelfEvalChange,MeanMotivation,MeanEnvy,MeanInspiration,MeanDiscouragement,MeanRelativeDeprivation");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.gap_sum / n,
            s.attainability_sum / n,
            s.eval_change_sum / n,
            s.motivation_sum / n,
            s.envy_sum / n,
            s.inspiration_sum / n,
            s.discouragement_sum / n,
            s.relative_deprivation_sum / n
        );
    }
}
