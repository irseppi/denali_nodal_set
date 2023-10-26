use std::io::prelude::*;

struct Parser {
    line_count: usize,
    saved_lines: Vec<String>,
}
impl Parser {
    const SUBMIT_SIZE: usize = 1_000;
    pub fn new() -> Self {
        Self {
            line_count: 0,
            saved_lines: vec![],
        }
    }
    fn build_val_str(line: &str) -> Option<String> {
        if line.chars().next() == Some('|') {
            let line = line
                .split('|')
                .map(|s| s.trim())
                .filter(|s| s != &"")
                .collect::<Vec<_>>();
            if line[0] == "time" || line.len() != 17 {
                return None;
            }

            Some(format!(
                "({},\"{}\",{},{},{},{},{},\"{}\",{},{},{},\"{}\",{},{},{},{},{})",
                line[0],
                line[1],
                line[2],
                line[3],
                line[4],
                line[5],
                line[6],
                line[7],
                line[8],
                line[9],
                line[10],
                line[11],
                line[12],
                line[13],
                line[14],
                line[15],
                line[16]
            ))
        } else {
            None
        }
    }
    fn submit_lines(&mut self, connection: &sqlite::Connection) {
        let submit_header = "INSERT INTO planes \
            (time, icao24, \
            lat, lon,velocity, heading,\
            vertrate,callsign, \
            onground, alert, \
            spi, squawk,\
            boraltitude, geoaltitude,\
            lastposupdate,\
            lastcontact, hour) VALUES "
            .to_string();
        let submit_body = self
            .saved_lines
            .iter()
            .map(|line| Self::build_val_str(line))
            .flatten()
            .fold(
                String::new(),
                |acc, x| if acc != "" { acc + "," + &x } else { x },
            )
            + ";";
        if submit_body != ";" {
            let exec_str = submit_header + &submit_body;
            if let Some(err) = connection.execute(exec_str.clone()).err() {
                panic!("bad exec string: {} with error\n{}", exec_str, err);
            }
        }
    }

    pub fn parse_line(&mut self, line: String, connection: &sqlite::Connection) {
        if self.line_count <= 12 {
            println!("line[{}]: {}", self.line_count, line);
        }

        if self.line_count >= 11 {
            self.saved_lines.push(line);
            if self.saved_lines.len() == Self::SUBMIT_SIZE {
                self.submit_lines(connection);
                self.saved_lines.clear();
            }
        }

        // parse line

        if self.line_count % 10_000 == 0 {
            println!("{}", self.line_count);
        }
        self.line_count += 1
    }
}
fn main() {
    let connection =
        sqlite::open("/scratch/naalexeev/flight_database_new.sqlite").expect("failed to open db");
    connection
        .execute(
            "CREATE TABLE planes (time REAL, icao24 TEXT, \
            lat REAL, lon Real,velocity REAL, heading REAL,\
            vertrate REAL,callsign TEXT, \
            onground INTEGER, alert INTEGER, \
            spi INTEGER, squawk TEXT,\
            boraltitude REAL, geoaltitude REAL,\
            lastposupdate REAL,\
            lastcontact REAL, hour INTEGER);",
        )
        .unwrap();
    let mut parser = Parser::new();
    let mut f =
        std::fs::File::open("/scratch/naalexeev/NODAL/log.txt").expect("failed to load file");
    let mut buff = [0u8; 3000];

    let mut current_line = String::new();
    loop {
        let read_count = f.read(&mut buff).expect("failed to read");
        if read_count == 0 {
            break;
        }
        let mut temp_string = String::from_utf8(buff.to_vec()).expect("failed to make");
        for (idx, c) in temp_string.chars().enumerate() {
            if c != '\n' {
                current_line.push(c);
            } else {
                current_line.push(c);
                parser.parse_line(current_line.clone(), &connection);

                current_line.clear();
            }
        }
    }

    println!("line count: {}", parser.line_count);
}
