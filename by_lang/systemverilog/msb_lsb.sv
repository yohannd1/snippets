// Some MSB-LSB indexing tests.

module msb_lsb;
  // The declaration syntax for packed arrays is [MSB:LSB].
  logic[7:0] a = 43;
  logic[0:7] b = 43;

  initial begin
    // the numerical interpretation seems to be the same for both:
    $display("a = %b (%d)", a, a);
    $display("b = %b (%d)", b, b);
    $display();

    // indexing is different, and it makes sense:
    // in a: a[0] is the LSB, which is 1
    // in b: a[0] is the MSB, which is 0
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
    // the slice, it has the same order of bits as the 
    $display("a[3:0]=%b b[0:3]=%b", a[3:0], b[0:3]);
    $display();

    $finish;
  end
endmodule
