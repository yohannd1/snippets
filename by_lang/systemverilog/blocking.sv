// A comparation of blocking and non-blocking assignments.

module nonblocking(input clk, input n_rst);
  logic[7:0] x, y;

  always @(posedge clk, negedge n_rst) begin
    if (~n_rst) begin
      x <= 0;
      y <= 0;
    end else begin
      x <= x + 1;
      y <= x;
    end
  end
endmodule

module blocking(input clk, input n_rst);
  logic[7:0] x, y;

  always @(posedge clk, negedge n_rst) begin
    if (~n_rst) begin
      x = 0;
      y = 0;
    end else begin
      x = x + 1;
      y = x;
    end
  end
endmodule

`timescale 1ns/1ns

module m_top;
  logic clk, n_rst;
  nonblocking nb_u0(.*);
  blocking b_u0(.*);

  localparam T = 2;

  initial begin: clock
    clk = 0;
    forever #(T/2) clk = ~clk;
  end

  initial begin: stimulus
    n_rst = 0;
    @(negedge clk);

    n_rst = 1;
    repeat(4) @(negedge clk);

    // Non-blocking assignment: y receives the "old value" of x
    assert(nb_u0.x == 4 && nb_u0.y == 3);

    // Blocking assignment: y receives the value of x after it being updated,
    // in the same cycle.
    assert(b_u0.x == 4 && b_u0.y == 4);

    $finish;
  end
endmodule
