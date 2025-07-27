// Not fully sure yet what automatic functions mean. TODO
// But I think it's like, they can each have their own local variables and
// internal state? declaring a non-static variable inside it only works if
// it's automatic.
//
// By the way, it's not available on every version (TODO: which version does
// it start being available at)

module m_top;
  localparam X = 10;
  integer a;

  function automatic integer value();
    integer localx = a + X;
    return localx;
  endfunction

  initial begin
    a = 5;
    $display("Hello, world! value() = %0d", value());
    $finish;
  end
endmodule
