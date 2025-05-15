mod token;

use std::io::{self, Write};
use token::{tokenize, Token};

fn main() -> io::Result<()> {
    let mut buffer = String::new();
    let mut stdin = io::stdin();
    let mut stdout = io::stdout();

    loop {
        print!("> ");
        stdout.flush();
        stdin.read_line(&mut buffer)?;

        let tokens = tokenize(&buffer).expect("failed to parse");
        println!("TOKENIZED: {:?}", tokens);
        let mut tree: Vec<Pratt> = tokens.iter().map(|&x| Pratt::Token(x)).collect();
        pratt_make_tree(&mut tree);
        println!("TREE: {:?}", tree);

        buffer.clear();
    }

    Ok(())
}

#[derive(Debug, Clone)]
enum Pratt {
    Token(Token),
    OpTree {
        left: Box<Pratt>,
        right: Box<Pratt>,
        op: char,
    },
}

fn pratt_make_tree(tree: &mut Vec<Pratt>) {
    for p in 1..=2 {
        let mut i = 0;
        while i < tree.len() {
            if let Pratt::Token(Token::BinOp(op)) = tree[i] {
                if priority(op) == p {
                    if i == 0 {
                        panic!("no value on the left...")
                    }
                    if let Pratt::Token(Token::BinOp(_)) = tree[i - 1] {
                        panic!("fuck");
                    }
                    if i == tree.len() - 1 {
                        panic!("no value on the right...")
                    }
                    if let Pratt::Token(Token::BinOp(_)) = tree[i + 1] {
                        panic!("fuck");
                    }

                    let l = tree.remove(i - 1);
                    let r = tree.remove(i);

                    // at this point, the BinOp is at tree[i - 1], and we can just replace it with
                    // the new one
                    tree[i - 1] = Pratt::OpTree {
                        left: Box::new(l),
                        right: Box::new(r),
                        op: op,
                    };

                    // don't increment i - it's already at the new "next" index
                } else {
                    i += 1;
                }
            } else {
                i += 1;
            }
        }
    }
}

fn priority(op: char) -> i32 {
    // the lower the number, the higher the priority
    match op {
        '*' | '/' => 1,
        '+' | '-' => 2,
        _ => panic!("whoops"),
    }
}
