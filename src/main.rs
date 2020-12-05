mod client;
use client::Client;
use log::info;
use std::error::Error;
use std::io::Write;

extern crate env_logger;
extern crate rand;

use chrono::Local;
use env_logger::Builder;
use log::LevelFilter;

use rand::distributions::Alphanumeric;
use rand::Rng;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    Builder::new()
        .format(|buf, record| {
            writeln!(
                buf,
                "{} [{}] - {}",
                Local::now().format("%Y-%m-%dT%H:%M:%S:%f"),
                record.level(),
                record.args()
            )
        })
        .filter(None, LevelFilter::Info)
        .init();

    let mut game_client = Client::new("localhost".to_string(), "8081".to_string());

    let name = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(10)
        .collect::<String>();

    info!("Started a client for a team: {}", name);

    let color = game_client.connect(name).await.unwrap();

    let moves: Vec<u32> = if color == "RED" {
        vec![9, 13]
    } else {
        vec![24, 20]
    };

    game_client.make_move(moves).await.unwrap();

    let _ = game_client.game_info().await.unwrap();

    let moves: Vec<u32> = if color == "RED" {
        vec![10, 14]
    } else {
        vec![21, 17]
    };

    game_client.make_move(moves).await.unwrap();

    let _ = game_client.game_info().await.unwrap();

    Ok(())
}
