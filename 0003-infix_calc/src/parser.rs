use crate::token::{priority, Token};

// TODO: optimize stack usage (I think it's O(n) here... though maybe tail call optimization helps)

#[derive(Debug, Clone)]
pub enum Node {
    Int(i32),
    BinOp {
        left: Box<Node>,
        right: Box<Node>,
        op: char,
    },
}

pub fn parse(tokens: &[Token]) -> Option<Node> {
    match tokens.get(0) {
        Some(Token::Int(i)) => Some(inner_parse(Node::Int(*i), &tokens[1..])),
        Some(Token::BinOp(_)) => panic!("unexpected binary operator"),
        None => None,
    }
}

fn inner_parse(lhs: Node, rest: &[Token]) -> Node {
    let op = match rest.get(0) {
        Some(Token::BinOp(op)) => *op,
        Some(Token::Int(_)) => panic!("unexpected int"),
        None => return lhs,
    };

    let rval = match rest.get(1) {
        Some(Token::BinOp(_)) => panic!("unexpected binary operator"),
        Some(Token::Int(i)) => *i,
        None => panic!("unexpected end of input"),
    };

    match rest.get(2) {
        Some(Token::BinOp(op2)) => {
            if priority(op) <= priority(*op2) {
                // the current operation has higher or equal priority
                inner_parse(
                    Node::BinOp {
                        left: Box::new(lhs),
                        right: Box::new(Node::Int(rval)),
                        op: op,
                    },
                    &rest[2..],
                )
            } else {
                // we need to do the next operation first, and we can be sure it'll handle the ones
                // to its right too
                Node::BinOp {
                    left: Box::new(lhs),
                    right: Box::new(inner_parse(Node::Int(rval), &rest[2..])),
                    op: op,
                }
            }
        }
        Some(Token::Int(_)) => panic!("unexpected int"),
        None => Node::BinOp {
            left: Box::new(lhs),
            right: Box::new(Node::Int(rval)),
            op: op
        },
    }
}
