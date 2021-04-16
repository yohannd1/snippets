use std::sync::mpsc;
use std::thread;
use std::time::Duration;

#[derive(Debug)]
enum Message {
    UpdateScreen,
}

fn main() {
    let (th1, rh) = mpsc::channel();
    let th2 = th1.clone();

    thread::spawn(move || {
        loop {
            th1.send(Message::UpdateScreen).unwrap();
            thread::sleep(Duration::from_secs(5));
        }
    });

    thread::spawn(move || {
        use std::io::BufRead;
        use std::io;

        for _ in io::stdin().lock().lines() {
            th2.send(Message::UpdateScreen).unwrap();
        }
    });

    println!("START");

    for message in rh {
        println!("{:?}", message);
    }

    println!("END");
}
