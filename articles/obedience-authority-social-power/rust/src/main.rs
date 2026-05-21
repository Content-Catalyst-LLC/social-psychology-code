use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Default, Debug)]
struct Summary {
    n: usize,
    obeyed_sum: f64,
    resisted_sum: f64,
    authority_sum: f64,
    moral_sum: f64,
    hesitation_sum: f64,
}

fn parse_f64(value: &str) -> f64 {
    value.parse::<f64>().unwrap_or(f64::NAN)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/obedience_trials.csv");
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
    let context_i = idx("institution_context");
    let obeyed_i = idx("obeyed");
    let resisted_i = idx("resisted");
    let legitimacy_i = idx("authority_legitimacy");
    let prox_i = idx("authority_proximity");
    let prestige_i = idx("institutional_prestige");
    let command_i = idx("command_clarity");
    let cost_i = idx("cost_of_defiance");
    let peercomp_i = idx("peer_compliance");
    let dissent_i = idx("peer_dissent");
    let moral_i = idx("moral_conflict");
    let victim_i = idx("victim_proximity");
    let harm_i = idx("harm_salience");
    let responsibility_i = idx("perceived_responsibility_after");
    let hesitation_i = idx("hesitation");

    let mut summaries: HashMap<String, Summary> = HashMap::new();

    for line in lines {
        if line.trim().is_empty() {
            continue;
        }
        let fields: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", fields[condition_i], fields[context_i]);

        let authority_pressure = (
            parse_f64(fields[legitimacy_i])
            + parse_f64(fields[prox_i])
            + parse_f64(fields[prestige_i])
            + parse_f64(fields[command_i])
            + parse_f64(fields[cost_i])
            + parse_f64(fields[peercomp_i])
            - parse_f64(fields[dissent_i])
        ) / 6.0;

        let moral_resistance = (
            parse_f64(fields[moral_i])
            + parse_f64(fields[victim_i])
            + parse_f64(fields[harm_i])
            + parse_f64(fields[dissent_i])
            + parse_f64(fields[responsibility_i])
        ) / 5.0;

        let entry = summaries.entry(key).or_default();
        entry.n += 1;
        entry.obeyed_sum += parse_f64(fields[obeyed_i]);
        entry.resisted_sum += parse_f64(fields[resisted_i]);
        entry.authority_sum += authority_pressure;
        entry.moral_sum += moral_resistance;
        entry.hesitation_sum += parse_f64(fields[hesitation_i]);
    }

    println!("ConditionContext,Trials,ObedienceRate,ResistanceRate,MeanAuthorityPressure,MeanMoralResistance,MeanHesitation");

    let mut keys: Vec<String> = summaries.keys().cloned().collect();
    keys.sort();

    for key in keys {
        let s = summaries.get(&key).unwrap();
        let n = s.n as f64;
        println!(
            "{},{},{:.3},{:.3},{:.3},{:.3},{:.3}",
            key,
            s.n,
            s.obeyed_sum / n,
            s.resisted_sum / n,
            s.authority_sum / n,
            s.moral_sum / n,
            s.hesitation_sum / n
        );
    }
}
