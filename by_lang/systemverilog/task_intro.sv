// TODO: differentiate tasks from functions...

module task_intro;
  integer x;

  // Simple tasks to inc. by 2, without receiving parameters.
  task inc2_v1();
    x = x + 2;
  endtask

  // Simple tasks to inc. by 2, explicitly having an input and output
  task inc2_v2(input integer x_in, output integer x_out);
    x_out = x_in + 2;
  endtask

  // TODO: example with `ref`

  initial begin
    x = 1;
    $display("x=%0d", x);
    inc2_v1();
    $display("x=%0d", x);
    inc2_v2(x, x);
    $display("x=%0d", x);
    $finish;
  end
endmodule
