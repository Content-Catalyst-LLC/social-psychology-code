use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    contact_quality_sum: f64,
    allport_quality_sum: f64,
    negative_contact_sum: f64,
    anxiety_sum: f64,
    empathy_sum: f64,
    trust_sum: f64,
    pre_sum: f64,
    post_sum: f64,
    social_distance_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/contact_hypothesis_trials.csv");
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
    let contact_quality_i = idx("contact_quality");
    let equal_i = idx("equal_status");
    let goals_i = idx("common_goals");
    let coop_i = idx("cooperation");
    let support_i = idx("institutional_support");
    let voluntariness_i = idx("voluntariness");
    let negative_i = idx("negative_contact");
    let anxiety_i = idx("intergroup_anxiety");
    let empathy_i = idx("empathy");
    let trust_i = idx("trust");
    let pre_i = idx("prejudice_pre");
    let post_i = idx("prejudice_post");
    let social_distance_i = idx("social_distance");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let condition = fields[condition_i].to_string();
        let entry = summaries.entry(condition).or_default();
        entry.n += 1;
        entry.contact_quality_sum += parse_f64(fields[contact_quality_i]);
        entry.allport_quality_sum += (
            parse_f64(fields[equal_i]) + parse_f64(fields[goals_i]) +
            parse_f64(fields[coop_i]) + parse_f64(fields[support_i]) +
            parse_f64(fields[voluntariness_i])
        ) / 5.0;
        entry.negative_contact_sum += parse_f64(fields[negative_i]);
        entry.anxiety_sum += parse_f64(fields[anxiety_i]);
        entry.empathy_sum += parse_f64(fields[empathy_i]);
        entry.trust_sum += parse_f64(fields[trust_i]);
        entry.pre_sum += parse_f64(fields[pre_i]);
        entry.post_sum += parse_f64(fields[post_i]);
        entry.social_distance_sum += parse_f64(fields[social_distance_i]);
    }

    println!("Condition,Trials,MeanContactQuality,MeanAllportQuality,MeanNegativeContact,MeanAnxiety,MeanEmpathy,MeanTrust,MeanPrejudicePre,MeanPrejudicePost,MeanPrejudiceChange,MeanSocialDistance");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.contact_quality_sum / n,
            s.allport_quality_sum / n,
            s.negative_contact_sum / n,
            s.anxiety_sum / n,
            s.empathy_sum / n,
            s.trust_sum / n,
            s.pre_sum / n,
            s.post_sum / n,
            (s.post_sum - s.pre_sum) / n,
            s.social_distance_sum / n
        );
    }
}
