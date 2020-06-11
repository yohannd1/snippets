struct Object {
    pos: f32,
}

fn main() {
    let obj1 = Object::new(10.3);
    let obj2 = Object::new(4.5);

    println!("Distance: {}", obj1.distance_to(&obj2));
}

impl Object {
    #[inline]
    pub fn distance_to(&self, other: &Object) -> f32 {
        other.pos - self.pos
    }

    pub fn new(pos: f32) -> Self {
        Object { pos }
    }
}
