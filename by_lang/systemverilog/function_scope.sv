// It seems functions can access the upper scope, both modifying and reading
// values. It seems like this is generally frowned upon, though, due to
// implicit dependencies and race condition potential.

module m_top;
  localparam X = 10;
  integer a;
  integer b;

  function integer value();
    b = a + X;
    return b;
  endfunction

  initial begin
    a = 5;
    $display("Hello, world! value() = %0d", value());
    $finish;
  end
endmodule
