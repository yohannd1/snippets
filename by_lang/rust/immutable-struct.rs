//! A failed attempt at forcing data to be immutable, even in mutable references.
//!
//! Doesn't work well because, if you have a &mut T, you can do as in below:
//!
//! ```rust
//! let mut shouldntwork = Immut::new(20);
//! *shouldntwork = Immut::new(25);
//! ```

/// Stores "immutable" data.
///
/// See module level documentation for more details.
pub struct Imut<T>(T);

impl<T> Imut<T> {
    #[inline]
    pub fn new(inner: T) -> Self {
        Self(inner)
    }

    #[inline]
    pub fn inner(&self) -> &T {
        &self.0
    }

    #[inline]
    pub fn consume(self) -> T {
        self.0
    }
}

impl<T> AsRef<T> for Imut<T> {
    fn as_ref(&self) -> &T {
        self.inner()
    }
}

impl<T> std::ops::Deref for Imut<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        self.inner()
    }
}

impl<T> From<T> for Imut<T> {
    fn from(inner: T) -> Self {
        Self::new(inner)
    }
}

impl<T> Into<T> for Imut<T> {
    fn into(self) -> T {
        self.consume()
    }
}

fn main() {}
