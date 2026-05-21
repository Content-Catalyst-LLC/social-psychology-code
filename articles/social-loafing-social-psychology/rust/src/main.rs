use std::{collections::HashMap, env, fs};

#[derive(Default)]
struct S { n: usize, effort_loss: f64, motivation_loss: f64, output: f64, accountability: f64, identifiability: f64 }

fn val(s: &str) -> f64 { s.parse::<f64>().unwrap_or(f64::NAN) }

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: cargo run --manifest-path rust/Cargo.toml -- data/social_loafing_trials.csv");
        std::process::exit(1);
    }
    let content = fs::read_to_string(&args[1]).expect("Could not read CSV");
    let mut lines = content.lines();
    let headers: Vec<&str> = lines.next().expect("Missing header").split(',').collect();
    let idx = |name: &str| headers.iter().position(|h| *h == name).expect(name);
    let condition = idx("condition");
    let task = idx("task_type");
    let effort_loss = idx("effort_loss");
    let motivation_loss = idx("motivation_loss");
    let output = idx("output_score");
    let accountability = idx("accountability");
    let identifiability = idx("identifiability");

    let mut map: HashMap<String, S> = HashMap::new();
    for line in lines {
        if line.trim().is_empty() { continue; }
        let f: Vec<&str> = line.split(',').collect();
        let key = format!("{}:{}", f[condition], f[task]);
        let e = map.entry(key).or_default();
        e.n += 1;
        e.effort_loss += val(f[effort_loss]);
        e.motivation_loss += val(f[motivation_loss]);
        e.output += val(f[output]);
        e.accountability += val(f[accountability]);
        e.identifiability += val(f[identifiability]);
    }
    println!("ConditionTask,Trials,MeanEffortLoss,MeanMotivationLoss,MeanOutput,MeanAccountability,MeanIdentifiability");
    let mut keys: Vec<String> = map.keys().cloned().collect();
    keys.sort();
    for k in keys {
        let s = map.get(&k).unwrap();
        let n = s.n as f64;
        println!("{},{},{:.3},{:.3},{:.3},{:.3},{:.3}", k, s.n, s.effort_loss/n, s.motivation_loss/n, s.output/n, s.accountability/n, s.identifiability/n);
    }
}
