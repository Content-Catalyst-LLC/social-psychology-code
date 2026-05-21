use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Blocks {
    congruent_sum: f64,
    congruent_n: usize,
    incongruent_sum: f64,
    incongruent_n: usize,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/implicit_bias_trials.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Could not read CSV file");
    let mut lines = content.lines();
    let header_line = lines.next().expect("Missing header");
    let headers: Vec<&str> = header_line.split(',').collect();

    let idx = |name: &str| -> usize {
        headers.iter().position(|h| *h == name).unwrap_or_else(|| panic!("Missing column: {}", name))
    };

    let participant_i = idx("participant");
    let condition_i = idx("condition");
    let congruent_i = idx("congruent_block");
    let rt_i = idx("response_time_ms");
    let accuracy_i = idx("accuracy");

    let mut blocks: HashMap<String, Blocks> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let accuracy = parse_f64(fields[accuracy_i]);
        if accuracy < 1.0 {
            continue;
        }
        let key = format!("{}:{}", fields[participant_i], fields[condition_i]);
        let rt = parse_f64(fields[rt_i]);
        let congruent = parse_f64(fields[congruent_i]);

        let entry = blocks.entry(key).or_default();
        if congruent >= 1.0 {
            entry.congruent_sum += rt;
            entry.congruent_n += 1;
        } else {
            entry.incongruent_sum += rt;
            entry.incongruent_n += 1;
        }
    }

    println!("ParticipantCondition,MeanCongruentRT,MeanIncongruentRT,SimpleDifference");

    let mut keys: Vec<String> = blocks.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let b = blocks.get(&key).unwrap();
        if b.congruent_n > 0 && b.incongruent_n > 0 {
            let congruent = b.congruent_sum / b.congruent_n as f64;
            let incongruent = b.incongruent_sum / b.incongruent_n as f64;
            println!("{},{:.3},{:.3},{:.3}", key, congruent, incongruent, incongruent - congruent);
        }
    }
}
