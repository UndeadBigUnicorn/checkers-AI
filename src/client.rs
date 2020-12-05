extern crate reqwest;
use log::{info, warn};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::fmt;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error + Send + Sync>>;
#[derive(Debug)]
struct ClientError(String);

impl fmt::Display for ClientError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "There is an error: {}", self.0)
    }
}

impl std::error::Error for ClientError {}

pub struct Client {
    host: String,
    port: String,
    token: Option<String>,
}

impl Client {
    pub fn new(host: String, port: String) -> Client {
        Client {
            host,
            port,
            token: None,
        }
    }

    pub async fn game_info(&self) -> Result<GameInfoResp> {
        info!("Getting game info...");
        let res = reqwest::get(&format!("http://{}:{}/game", self.host, self.port)).await?;
        let game_info = res.json::<GameInfoResp>().await?;
        info!("Got game info: {:?}", game_info);
        Ok(game_info)
    }

    pub async fn connect(&mut self, name: String) -> Result<String> {
        info!("Connecting to the game server...");
        let res = reqwest::Client::new()
            .post(&format!(
                "http://{}:{}/game?team_name={}",
                self.host, self.port, name
            ))
            .send()
            .await
            .unwrap();

        if res.status().is_success() {
            let data_payload = res.json::<ConnectResp>().await.unwrap();
            let data = data_payload.data;

            self.token = Some(data.token);
            info!(
                "Connected to a server and got assigned color: {}",
                data.color
            );
            Ok(data.color)
        } else {
            let err = res.text().await.unwrap().to_owned();
            warn!("Error while connecting to the server: '{}'", err);
            // Err(Box::new(ClientError(err)))
            Err(err)?
        }
    }

    pub async fn make_move(&self, moves: Vec<u32>) -> Result<()> {
        info!("Making moves...");
        let res = reqwest::Client::new()
            .post(&format!("http://{}:{}/move", self.host, self.port))
            .header(
                "Authorization",
                format!("Token {}", self.token.as_ref().unwrap()),
            )
            .json(&json!({ "move": &moves }))
            .send()
            .await
            .unwrap();

        if res.status().is_success() {
            info!("Made moves: {:?}", moves);
            Ok(())
        } else {
            let err = res.text().await.unwrap().to_owned();
            warn!("Error while making moves: '{}'", err);
            // Err(Box::new(ClientError(err)))
            Err(err)?
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct ConnectResp {
    status: String,
    data: ConnectRespData,
}

#[derive(Debug, Serialize, Deserialize)]
struct ConnectRespData {
    token: String,
    color: String,
}


#[derive(Debug, Serialize, Deserialize)]
pub struct GameInfoResp {
    status: String,
    pub data: GameInfoData,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct GameInfoData {
    pub status: String,
    pub whose_turn: String,
    pub winner: Option<String>,
    pub board: Vec<Cell>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Cell {
    pub color: String,
    pub row: u32,
    pub column: u32,
    pub king: bool,
    pub position: u32,
}
