use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    md_sum: f64,
    harmful_sum: f64,
    policy_sum: f64,
    intention_sum: f64,
    empathy_sum: f64,
    guilt_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/moral_disengagement_trials.csv");
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
    let domain_i = idx("scenario_domain");
    let mechanisms = [
        idx("moral_justification"),
        idx("euphemistic_labeling"),
        idx("advantageous_comparison"),
        idx("displaced_responsibility"),
        idx("diffused_responsibility"),
        idx("consequence_distortion"),
        idx("dehumanization"),
        idx("blame_attribution"),
    ];
    let harmful_i = idx("harmful_decision");
    let policy_i = idx("policy_endorsement");
    let intention_i = idx("unethical_intention");
    let empathy_i = idx("empathy");
    let guilt_i = idx("guilt");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[domain_i]);
        let entry = summaries.entry(key).or_default();
        entry.n += 1;

        let mut md = 0.0;
        for i in mechanisms {
            md += parse_f64(fields[i]);
        }
        md /= 8.0;

        entry.md_sum += md;
        entry.harmful_sum += parse_f64(fields[harmful_i]);
        entry.policy_sum += parse_f64(fields[policy_i]);
        entry.intention_sum += parse_f64(fields[intention_i]);
        entry.empathy_sum += parse_f64(fields[empathy_i]);
        entry.guilt_sum += parse_f64(fields[guilt_i]);
    }

    println!("ConditionDomain,Trials,MeanMD,HarmfulRate,MeanPolicyEndorsement,MeanUnethicalIntention,MeanEmpathy,MeanGuilt");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.md_sum / n,
            s.harmful_sum / n,
            s.policy_sum / n,
            s.intention_sum / n,
            s.empathy_sum / n,
            s.guilt_sum / n
        );
    }
}
