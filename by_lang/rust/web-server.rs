//! A sample web server and thread pool based off the rust book's 12nd chapter -
//! https://doc.rust-lang.org/stable/book/ch20-00-final-project-a-web-server.html

use std::io::prelude::*;
use std::net::{TcpListener, TcpStream};
use std::error::Error;

use thread_pool::ThreadPool;

mod thread_pool {
    use std::sync::{mpsc, Arc, Mutex};
    use std::thread;

    pub struct ThreadPool {
        workers: Vec<Worker>,
        sender: mpsc::Sender<Message>,
    }

    pub enum Message {
        NewJob(Box<dyn FnOnce() + Send + 'static>),
        Stop,
    }

    impl ThreadPool {
        pub fn new(amount: usize) -> Self {
            let (sender, receiver) = mpsc::channel();
            let receiver = Arc::new(Mutex::new(receiver));

            let mut workers = Vec::with_capacity(amount);

            for id in 0..amount {
                workers.push(Worker::new(id, Arc::clone(&receiver)));
            }

            Self { workers, sender }
        }

        pub fn execute<F>(&self, f: F)
        where
            F: FnOnce() + Send + 'static,
        {
            let job = Box::new(f);

            self.sender.send(Message::NewJob(job)).unwrap();
        }
    }

    impl Drop for ThreadPool {
        fn drop(&mut self) {
            println!("Shutting down all workers...");

            for _ in &self.workers {
                self.sender.send(Message::Stop).unwrap();
            }

            for worker in &mut self.workers {
                println!("Shutting down worker {}", worker.id);

                if let Some(thread) = worker.thread.take() {
                    thread.join().unwrap();
                }
            }
        }
    }

    struct Worker {
        id: usize,
        thread: Option<thread::JoinHandle<()>>,
    }

    impl Worker {
        pub fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Message>>>) -> Self {
            let thread = thread::spawn(move || loop {
                println!("Worker #{} ready!", id);

                let message = receiver.lock().unwrap().recv().unwrap();
                match message {
                    Message::NewJob(job) => {
                        println!("Worker #{} started executing a job.", id);
                        job();
                    }
                    Message::Stop => {
                        println!("Worker #{} was shut down.", id);
                        break;
                    }
                }
            });

            Self { id, thread :Some(thread) }
        }
    }
}

fn main() {
    println!("Starting server!");

    let listener = TcpListener::bind("10.147.18.25:7878").unwrap();
    let thread_pool = ThreadPool::new(4);

    for stream in listener.incoming() {
        thread_pool.execute(|| {
            // thread::sleep(Duration::from_secs(5));
            if let Err(err) = handle_connection(stream.unwrap()) {
                print!("An error ocurred while handling a connection:");
                println!(" * {}", err);
            }
        });
    }
}

fn handle_connection(mut stream: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut buffer: [u8; 1024] = [0; 1024];
    stream.read(&mut buffer)?;
    println!("Request: {}", String::from_utf8_lossy(&buffer[..]));

    if is_root_get_request(&buffer) {
        let content = simple_html_page("Success!");
        let response = format!(
            "HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n{}",
            content.len(),
            content,
        );

        stream.write(response.as_bytes())?;
        stream.flush()?;
    } else {
        let status = "HTTP/1.1 404 NOT FOUND\r\n\r\n";
        let content = simple_html_page("404 - Not Found");
        stream.write(status.as_bytes())?;
        stream.write(content.as_bytes())?;
        stream.flush().unwrap();
    }

    Ok(())
}

fn simple_html_page(content: &str) -> String {
    format!(
        r#"<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Hello!</title>
    </head>
    <body>
        <p>{}</p>
    </body>
</html>"#,
        content
    )
}

fn is_root_get_request(buffer: &[u8]) -> bool {
    buffer.starts_with(b"GET / HTTP/1.1\r\n")
}
