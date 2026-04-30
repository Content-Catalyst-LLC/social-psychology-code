fn attribution(dispositional: f64, situational: f64, w_d: f64, w_s: f64) -> f64 {
    w_d * dispositional + w_s * situational
}

fn main() {
    let score = attribution(0.8, 0.3, 0.7, 0.3);
    println!("Attribution score: {:.3}", score);
}
