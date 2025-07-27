#[derive(Debug, Clone, Copy)]
pub enum Token {
    Int(i32),
    BinOp(char),
}

pub fn tokenize(input: &str) -> Option<Vec<Token>> {
    let mut ret = vec![];
    let mut p = Tokenizer::new(input);

    loop {
        p.skip_whitespace();
        if let Some(x) = p.get_int() {
            ret.push(Token::Int(x));
        } else if let Some(x) = p.get_op() {
            ret.push(Token::BinOp(x));
        } else {
            break;
        }
    }

    p.expect_eof()?;
    Some(ret)
}

#[derive(Debug, Clone)]
struct Tokenizer<'a> {
    line: u32,
    column: u32,
    source: &'a str,
}

pub fn priority(op: char) -> i32 {
    // the lower the number, the higher the priority
    match op {
        '*' | '/' => 1,
        '+' | '-' => 2,
        _ => panic!("whoops"),
    }
}

impl<'a> Tokenizer<'a> {
    /// Create a new instance of the parser.
    ///
    /// Initializes the line and column to 1.
    pub fn new(source: &'a str) -> Self {
        Self {
            source,
            line: 1,
            column: 1,
        }
    }

    fn peek(&self) -> Option<char> {
        self.source.chars().next()
    }

    fn step(&mut self) {
        let Some(c) = self.peek() else {
            return;
        };

        if c == '\n' {
            self.line += 1;
            self.column = 1;
        } else {
            self.column += 1;
        }

        self.source = &self.source[1..];
    }

    fn count_while(&mut self, pred: impl Fn(char) -> bool) -> usize {
        let mut i = 0;
        while let Some(_) = self.peek().filter(|&c| pred(c)) {
            i += 1;
            self.step();
        }
        i
    }

    fn collect_while(&mut self, pred: impl Fn(char) -> bool) -> String {
        let mut ret = String::new();
        while let Some(c) = self.peek().filter(|&c| pred(c)) {
            ret.push(c);
            self.step();
        }
        ret
    }

    fn skip_whitespace(&mut self) {
        _ = self.count_while(|c| c == ' ' || c == '\n' || c == '\t');
    }

    fn expect_eof(&self) -> Option<()> {
        if self.peek().is_none() {
            Some(())
        } else {
            None
        }
    }

    pub fn get_int(&mut self) -> Option<i32> {
        let mut p = self.clone();

        let s = p.collect_while(Self::is_digit);
        if s.len() == 0 {
            return None;
        }

        let val = s.parse::<i32>().ok()?;
        *self = p;
        Some(val)
    }

    pub fn get_op(&mut self) -> Option<char> {
        let mut p = self.clone();

        match p.peek()? {
            c @ ('+' | '-' | '*' | '/') => {
                p.step();
                *self = p;
                Some(c)
            }
            _ => None,
        }
    }

    fn is_digit(c: char) -> bool {
        match c {
            '0'..='9' => true,
            _ => false,
        }
    }
}

