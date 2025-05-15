mod parser;
mod token;

use parser::{parse, Node};
use std::io::{self, Write};
use token::{tokenize, Token};

// TODO: support parens (might entail more refactoring...)
// TODO: proper error handling

fn main() -> io::Result<()> {
    let mut buffer = String::new();
    let mut stdin = io::stdin();
    let mut stdout = io::stdout();

    loop {
        print!("> ");
        stdout.flush()?;
        stdin.read_line(&mut buffer)?;

        let tokens = tokenize(&buffer).expect("failed to parse");
        println!("TOKENIZED: {:?}", tokens);

        let root = parse(&tokens);
        println!("TREE: {:?}", root);

        if let Some(n) = root {
            let result = eval(&n);
            println!("RESULT: {:?}", result);
        }

        buffer.clear();
    }
}

fn eval(node: &Node) -> i32 {
    match node {
        Node::Int(i) => *i,
        Node::BinOp { left, right, op } => match op {
            '+' => eval(&left) + eval(&right),
            '-' => eval(&left) - eval(&right),
            '*' => eval(&left) * eval(&right),
            '/' => eval(&left) / eval(&right),
            _ => panic!("unknown operator {:?}", op),
        },
    }
}
