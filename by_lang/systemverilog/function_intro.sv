module function_intro;
  function integer double(input integer x);
    return x + x;
  endfunction

  integer a;

  initial begin
    a = 10;
    $display("Hello, world! a = %0d, double(a) = %0d", a, double(a));
    $finish;
  end
endmodule
