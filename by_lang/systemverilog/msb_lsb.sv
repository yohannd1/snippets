// Some MSB-LSB indexing tests.

module msb_lsb;
  // The declaration syntax for packed arrays is [MSB index:LSB index]. The
  // total size of the packed array is |(MSB index) - (LSB index)| + 1.
  logic[7:0] a = 43;
  logic[0:7] b = 43;

  initial begin
    // the numerical interpretation seems to be the same for both:
    $display("Numerical interpretation:");
    $display("a = %b (%d)", a, a);
    $display("b = %b (%d)", b, b);
    $display();

    // indexing is different, and it makes sense:
    // in a: a[0] is the LSB, which is 1
    // in b: b[0] is the MSB, which is 0
    $display("Indexing:");
    $display("a[0]=%b b[0]=%b", a[0], b[0]);
    $display();

    // in a similar manner, slicing is also different between the two:
    //
    // in a: a[3:0] picks the 4 least significant bits
    //
    // in b: b[0:3] picks the 4 most significant bits - note it had to have
    // its slice order corrected!
    //
    // in the end, the slicing is always done in a way that, when you print
    // the slice, the relative order of the bits is the same as on the
    // original representation
    $display("Slicing:");
    $display("a[3:0]=%b b[0:3]=%b", a[3:0], b[0:3]);
    $display();

    // concatenation order is always MSB-to-LSB, indexes not mattering.
    //
    // in this example, though, i was doing a manual register shift, and thus
    // I had to take the slice indexes into account
    a = {a[6:0], 1'b0};
    b = {b[1:7], 1'b0};
    $display("Left shift via concatenation:");
    $display("a = %b", a);
    $display("b = %b", b);
    $display();

    // left shifts always multiply the number by a power of two, and right
    // shifts always divide them by a power of two
    a <<= 1;
    b <<= 1;
    $display("Left shift via `<<` operator:");
    $display("a = %b", a);
    $display("b = %b", b);
    $display();

    $finish;
  end
endmodule
